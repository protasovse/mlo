from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)


class QuestionLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10


class QuestionPageNumberPagination(PageNumberPagination):
    page_size = 10
