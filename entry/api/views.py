from django.db.models import Q

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)

from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from ..models import Question, Answer
from .pagination import QuestionLimitOffsetPagination, QuestionPageNumberPagination
from .permissions import (
    IsOwnerOrStaffOrReadOnly,
    IsLawyerReadOnly
)
from .serializers import (
    QuestionCreateUpdateSerializer,
    QuestionDetailSerializer,
    QuestionListSerializer,
    AnswerDetailSerializer,
    AnswerListSerializer,
    AnswerUpdateSerializer,
    answer_create_serializer)


class QuestionCreateAPIView(CreateAPIView):
    queryset = Question.published.all()
    serializer_class = QuestionCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class QuestionDetailAPIView(RetrieveAPIView):
    queryset = Question.published.all()
    serializer_class = QuestionDetailSerializer
    permission_classes = [AllowAny]


class QuestionUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Question.published.all()
    serializer_class = QuestionCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrStaffOrReadOnly]


class QuestionDeleteAPIView(DestroyAPIView):
    queryset = Question.published.all()
    serializer_class = QuestionDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrStaffOrReadOnly]


class QuestionListAPIView(ListAPIView):
    serializer_class = QuestionListSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        'title',
        'content',
        'author__first_name',
        'author__last_name',
        'author__patronymic',
        'author__email'
    ]
    pagination_class = QuestionPageNumberPagination  # PageNumberPagination

    def get_queryset(self):
        queryset = Question.published.all()
        # query = self.request.GET.get('q')
        #
        # if query:
        #     queryset = queryset.filter(
        #         Q(title__icontains=query)|
        #         Q(content__icontains=query)|
        #         Q(author__first_name__icontains=query)|
        #         Q(author__last_name__icontains=query)|
        #         Q(author__patronymic__icontains=query)|
        #         Q(author__email__icontains=query)
        #     ).distinct()

        return queryset


class AnswerDetailAPIView(RetrieveAPIView):
    queryset = Answer.published.all()
    serializer_class = AnswerDetailSerializer
    permission_classes = [AllowAny]


class AnswerListAPIView(ListAPIView):
    queryset = Answer.published.all()
    serializer_class = AnswerListSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = [
        'id',
        'content',
        'author__first_name',
        'author__last_name',
        'author__patronymic',
        'author__email'
    ]


class AnswerUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Answer.published.all()
    serializer_class = AnswerUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrStaffOrReadOnly]


class AnswerCreateAPIView(CreateAPIView):
    queryset = Answer.published.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        question_id = self.request.GET.get("question_id")
        answer_id = self.request.GET.get("answer_id", None)
        return answer_create_serializer(
                question_id=question_id,
                answer_id=answer_id,
                author=self.request.user
        )
