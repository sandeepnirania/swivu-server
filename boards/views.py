import json
import logging

from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.response import Response

from .models import Board
from .services import BoardLoadService, BryntumSyncService

logger = logging.getLogger(__name__)


class BoardActionView(views.APIView):

  def get(self, request, *args, **kwargs):
    board = self._get_board_and_check_permissions()
    service = BoardLoadService(board)
    response_data = service.load_all_data()
    return Response(response_data)

  def post(self, request, *args, **kwargs):
    board = self._get_board_and_check_permissions()
    service = BryntumSyncService(board)
    sync_data = json.loads(request.body.decode("utf-8"))
    response_data = service.process_sync(sync_data)
    return Response(response_data)

  def _get_board_and_check_permissions(self):
    slug = self.kwargs.get("slug")
    board = get_object_or_404(Board.objects.all(), slug=slug)
    # TODO: check permissions
    return board
