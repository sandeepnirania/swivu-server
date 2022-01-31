import math

from .models import Board
from .serializers import BoardSerializer
from assignments.serializers import AssignmentSerializer
from events.serializers import EventSerializer
from resources.serializers import ResourceSerializer
from revisions.models import Revision
from tasks.serializers import TaskSerializer


class BoardLoadService:

  def __init__(self, board):
    self.board = board

  def load_all_data(self):
    data = BoardSerializer(self.board).data
    for Serializer in (
        ResourceSerializer,
        TaskSerializer,
        EventSerializer,
        AssignmentSerializer,
    ):
      Model = Serializer.Meta.model
      store_name = Model._meta.verbose_name + "s"
      data[store_name] = {
          "rows": [Serializer(obj).data for obj in Model.objects.filter(board=self.board)]
      }
    return data


PHANTOM_ID_KEY = "$PhantomId"


class BryntumSyncService:

  def __init__(self, board):
    self.board = board

  def process_sync(self, sync_data):
    type = sync_data.get("type")
    if type is None:
      raise ValueError(f"Error: missing type")
    if type != "sync":
      raise ValueError(f"Error: invalid type {type}")

    request_id = sync_data.get("requestId")
    if request_id is None:
      raise ValueError(f"Error: missing requestId")
    try:
      if math.isnan(int(request_id)) or int(request_id) < 1:
        raise ValueError()
    except:
      raise ValueError(f"Error: invalid requestId {request_id}")
    request_id = int(request_id)

    new_models = {}

    def unphantom_ids(prop_dict):
      for key, value in prop_dict.items():
        if value in new_models:
          prop_dict[key] = new_models[value].id

    all_results = {}
    # Create new Tasks before the Events that refer to them.
    # Create new Events and Resources before the Assignments that refer to them.
    for Serializer in (
        ResourceSerializer,
        TaskSerializer,
        EventSerializer,
        AssignmentSerializer,
    ):
      Model = Serializer.Meta.model
      store_name = Model._meta.verbose_name + "s"
      store_sync_data = sync_data.get(store_name, {})
      store_results = {}
      for op in ("added", "updated", "removed"):
        for props in store_sync_data.get(op, []):
          props = props.copy()
          if op == "added":
            phantom_id = props.pop("$PhantomId", None)
            unphantom_ids(props)
            props["board"] = self.board.id
            serializer = Serializer(data=props)
            serializer.is_valid(raise_exception=True)
            model = serializer.save()
            result = serializer.data.copy()
            if phantom_id:
              new_models[phantom_id] = model
              result[PHANTOM_ID_KEY] = phantom_id
            result_key = "rows"
          else:
            id = props.pop("id")
            unphantom_ids(props)
            q = Model.objects.filter(board=self.board, id=id)
            if op == "updated":
              q.update(**props)
              result = Serializer(q.get()).data
              result_key = "rows"
            else:
              q.delete()
              result = {"id": id}
              result_key = "removed"
          if not store_results.get(result_key):
            store_results[result_key] = []
          store_results[result_key].append(result)

        if store_results.get("rows") or store_results.get("removed"):
          all_results[store_name] = store_results

    revision = Revision.objects.create(board=self.board, diff=all_results)
    all_results["success"] = True
    all_results["revision"] = revision.id
    all_results["requestId"] = request_id
    return all_results
