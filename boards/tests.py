from django.test import TestCase

from .models import Board
from .services import BryntumSyncService
from resources.models import Resource
from tasks.models import Task
from events.models import Event


class BoardSyncTestCase(TestCase):
  fixtures = ["test.json"]

  def test_initial_objects_counts(self):
    self.assertEquals(Board.objects.count(), 1)
    self.assertEquals(Resource.objects.count(), 5)
    self.assertEquals(Task.objects.count(), 4)
    self.assertEquals(Event.objects.count(), 10)

  def test_process_sync_1_error(self):
    service = BryntumSyncService(Board.objects.get(pk=1))
    with self.assertRaises(ValueError) as context:
      service.process_sync({})
    self.assertEquals(context.exception.args[0], "Error: missing type")

  def test_process_sync_2_error(self):
    service = BryntumSyncService(Board.objects.get(pk=1))
    with self.assertRaises(ValueError) as context:
      service.process_sync({"type": "toop"})
    self.assertEquals(context.exception.args[0], "Error: invalid type toop")

  def test_process_sync_3_error(self):
    service = BryntumSyncService(Board.objects.get(pk=1))
    with self.assertRaises(ValueError) as context:
      service.process_sync({"type": "sync"})
    self.assertEquals(context.exception.args[0], "Error: missing requestId")

  def test_process_sync_3_error(self):
    service = BryntumSyncService(Board.objects.get(pk=1))
    with self.assertRaises(ValueError) as context:
      service.process_sync({"type": "sync", "requestId": "NaN"})
    self.assertEquals(context.exception.args[0], "Error: invalid requestId NaN")

  def test_process_sync_empty(self):
    service = BryntumSyncService(Board.objects.get(pk=1))
    result = service.process_sync({"type": "sync", "requestId": 37})
    self.assertTrue(result)
    self.assertEquals(result["success"], True)
    self.assertEquals(result["requestId"], 37)

  def test_process_sync_added(self):
    service = BryntumSyncService(Board.objects.get(pk=1))
    result = service.process_sync({
        "type": "sync",
        "requestId": 38,
        "resources": {
            "added": [{
                "display_name": "Albert Einstein"
            }]
        },
        "tasks": {
            "added": [{
                "display_name": "General Relativity"
            }]
        }
    })
    self.assertTrue(result)
    self.assertEquals(result["success"], True)
    self.assertEquals(result["requestId"], 38)
    self.assertTrue(result["resources"])
    self.assertTrue(result["resources"]["rows"])
    self.assertTrue(result["resources"]["rows"][0]["id"])
    self.assertEquals(result["resources"]["rows"][0]["display_name"], "Albert Einstein")
    self.assertTrue(result["tasks"])
    self.assertTrue(result["tasks"]["rows"])
    self.assertTrue(result["tasks"]["rows"][0]["id"])
    self.assertEquals(result["tasks"]["rows"][0]["display_name"], "General Relativity")

  def test_process_sync_added_with_phantom_id(self):
    service = BryntumSyncService(Board.objects.get(pk=1))
    result = service.process_sync({
        "type": "sync",
        "requestId": 38,
        "events": {
            "added": [{
                "$PhantomId": "$p_new_event_1",
                "start_time": "2020-03-01",
                "end_time": "2020-03-02",
                "task": 1
            }]
        },
        "assignments": {
            "added": [{
                "event": "$p_new_event_1",
                "resource": 1
            }]
        }
    })
    self.assertTrue(result)
    self.assertEquals(result["success"], True)
    self.assertEquals(result["requestId"], 38)
    self.assertTrue(result["events"])
    self.assertTrue(result["events"]["rows"])
    self.assertTrue(result["events"]["rows"][0]["id"])
    self.assertEquals(result["events"]["rows"][0]["task"], 1)
    self.assertTrue(result["assignments"])
    self.assertTrue(result["assignments"]["rows"])
    self.assertTrue(result["assignments"]["rows"][0]["id"])
    self.assertEquals(result["assignments"]["rows"][0]["event"],
                      result["events"]["rows"][0]["id"])

  def test_process_sync_removed(self):
    prior_count = Event.objects.count()
    service = BryntumSyncService(Board.objects.get(pk=1))
    result = service.process_sync({
        "type": "sync",
        "requestId": 38,
        "events": {
            "removed": [{
                "id": 1
            }]
        }
    })
    self.assertTrue(result)
    self.assertEquals(result["success"], True)
    self.assertEquals(result["requestId"], 38)
    self.assertTrue(result["events"])
    self.assertTrue(result["events"]["removed"])
    self.assertEquals(result["events"]["removed"][0]["id"], 1)
    self.assertEquals(Event.objects.count(), prior_count - 1)

  def test_process_sync_updated(self):
    prior_count = Event.objects.count()
    service = BryntumSyncService(Board.objects.get(pk=1))
    result = service.process_sync({
        "type": "sync",
        "requestId": 40,
        "assignments": {
            "updated": [{
                "id": 1,
                "resource": 4
            }]
        }
    })
    self.assertTrue(result)
    self.assertEquals(result["success"], True)
    self.assertEquals(result["requestId"], 40)
    self.assertTrue(result["assignments"])
    self.assertTrue(result["assignments"]["rows"])
    self.assertEquals(result["assignments"]["rows"][0]["id"], 1)
    self.assertEquals(result["assignments"]["rows"][0]["resource"], 4)
    self.assertEquals(Event.objects.count(), prior_count)
