import logging

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import View

from .models import Board

logger = logging.getLogger(__name__)


class BoardSyncView(View):

    def post(self, request, *args, **kwargs):
        board_id = self.kwargs.get("board_id")
        board = get_object_or_404(Board.objects.filter(__user), )

        payload = dict([(k, v) for k, v in request.data.items()])

        logger.info(f"run_event_ingest {long_id} {headers} {payload}")
        run_event_ingest.delay(long_id, payload=payload, headers=headers)
        return HttpResponse()
