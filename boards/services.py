import math

from events.models import Event
from resources.models import Resource
from revisions.models import Revision
from tasks.models import Task


class BoardLoadService:

  def __init__(self, board):
    self.board = board

  def load_all_data(self):
    resources = [r.to_json() for r in Resources.objects.filter(board=self.board)]
    events = [e.to_json() for e in Events.objects.filter(board=self.board)]
    tasks = [t.to_json() for t in Tasks.objects.filter(board=self.board)]
    return {"resources": resources, "events": events, "tasks": tasks}


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

    all_results = {}
    for Model in (Event, Resource, Task):
      store_name = Model._meta.verbose_name + "s"
      store_sync_data = sync_data.get(store_name, {})
      store_results = {}
      for op in ("added", "updated", "removed"):
        for props in store_sync_data.get(op, []):
          if op == "added":
            model = Model.objects.create(board=self.board, **props)
            result = model.to_json()
            result_key = "rows"
          else:
            id = props.get("id")
            q = Model.objects.filter(board=self.board, id=id)
            if op == "updated":
              q.update(**props)
              result = q.get().to_json()
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
