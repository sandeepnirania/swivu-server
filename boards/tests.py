from django.test import TestCase

from .models import Board
from .services import BryntumSyncService
from resources.models import Resource
from tasks.models import Task
from events.models import Event


class BoardSyncTestCase(TestCase):
  fixtures = ["seed.json"]

  def test_initial_objects_counts(self):
    self.assertEquals(Board.objects.count(), 1)
    self.assertEquals(Resource.objects.count(), 5)
    self.assertEquals(Task.objects.count(), 3)
    self.assertEquals(Event.objects.count(), 10)

  def test_process_sync_0_error(self):
    with self.assertRaises(ValueError) as context:
      BryntumSyncService()
    self.assertEquals(context.exception.args[0], "Error: board or board_id required")

  def test_process_sync_1_error(self):
    service = BryntumSyncService(board=Board.objects.get(pk=1))
    with self.assertRaises(ValueError) as context:
      service.process_sync({})
    self.assertEquals(context.exception.args[0], "Error: missing type")

  def test_process_sync_2_error(self):
    service = BryntumSyncService(board=Board.objects.get(pk=1))
    with self.assertRaises(ValueError) as context:
      service.process_sync({"type": "toop"})
    self.assertEquals(context.exception.args[0], "Error: invalid type toop")

  def test_process_sync_3_error(self):
    service = BryntumSyncService(board=Board.objects.get(pk=1))
    with self.assertRaises(ValueError) as context:
      service.process_sync({"type": "sync"})
    self.assertEquals(context.exception.args[0], "Error: missing requestId")

  def test_process_sync_3_error(self):
    service = BryntumSyncService(board=Board.objects.get(pk=1))
    with self.assertRaises(ValueError) as context:
      service.process_sync({"type": "sync", "requestId": "NaN"})
    self.assertEquals(context.exception.args[0], "Error: invalid requestId NaN")

  def test_process_sync_empty(self):
    service = BryntumSyncService(board=Board.objects.get(pk=1))
    result = service.process_sync({"type": "sync", "requestId": 37})
    self.assertTrue(result)
    self.assertEquals(result["success"], True)
    self.assertEquals(result["requestId"], 37)

  def test_process_sync_added(self):
    service = BryntumSyncService(board=Board.objects.get(pk=1))
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

  def test_process_sync_removed(self):
    prior_count = Event.objects.count()
    service = BryntumSyncService(board=Board.objects.get(pk=1))
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
    service = BryntumSyncService(board=Board.objects.get(pk=1))
    result = service.process_sync({
        "type": "sync",
        "requestId": 40,
        "events": {
            "updated": [{
                "id": 1,
                "resource_id": 4
            }]
        }
    })
    self.assertTrue(result)
    self.assertEquals(result["success"], True)
    self.assertEquals(result["requestId"], 40)
    self.assertTrue(result["events"])
    self.assertTrue(result["events"]["rows"])
    self.assertEquals(result["events"]["rows"][0]["id"], 1)
    self.assertEquals(result["events"]["rows"][0]["resource_id"], 4)
    self.assertEquals(Event.objects.count(), prior_count)
