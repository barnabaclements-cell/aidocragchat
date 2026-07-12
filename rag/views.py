import os

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    UploadSerializer,
    ChatSerializer,
)

from .rag_service import (
    process_pdf,
    ask_question,
)


class UploadDocumentView(APIView):
    """
    Upload a PDF and build the vector database.
    """

    def post(self, request):

        serializer = UploadSerializer(data=request.data)

        if serializer.is_valid():

            uploaded_file = serializer.validated_data["file"]

            # Create upload directory if it doesn't exist
            os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

            # Save uploaded file
            file_path = os.path.join(
                settings.UPLOAD_DIR,
                uploaded_file.name
            )

            with open(file_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            try:
                total_chunks = process_pdf(file_path)

                return Response(
                    {
                        "message": "Document uploaded successfully.",
                        "filename": uploaded_file.name,
                        "chunks": total_chunks,
                    },
                    status=status.HTTP_201_CREATED,
                )

            except Exception as e:
                return Response(
                    {
                        "error": str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class ChatView(APIView):
    """
    Ask questions about the uploaded PDF.
    """

    def post(self, request):

        serializer = ChatSerializer(data=request.data)

        if serializer.is_valid():

            question = serializer.validated_data["question"]


            try:
                answer = ask_question(question)

                return Response(
                    {
                        "question": question,
                        "answer": answer,
                    },
                    status=status.HTTP_200_OK,
                )

            except Exception as e:
                return Response(
                    {
                        "error": str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )