"""Defines serializers used by the Proctoring API."""
from rest_framework import serializers
from django.contrib.auth.models import User
from edx_proctoring.models import ProctoredExam, ProctoredExamStudentAttempt, ProctoredExamStudentAllowance


class StrictBooleanField(serializers.BooleanField):
    """
    Boolean field serializer to cater for a bug in DRF BooleanField serializer
    where required=True is ignored.
    """
    def from_native(self, value):
        if value in ('true', 't', 'True', '1'):
            return True
        if value in ('false', 'f', 'False', '0'):
            return False
        return None


class ProctoredExamSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProctoredExam Model.
    """
    id = serializers.IntegerField(required=False)
    course_id = serializers.CharField(required=True)
    content_id = serializers.CharField(required=True)
    external_id = serializers.CharField(required=True)
    exam_name = serializers.CharField(required=True)
    time_limit_mins = serializers.IntegerField(required=True)

    is_active = StrictBooleanField(required=True)
    is_proctored = StrictBooleanField(required=True)

    class Meta:
        """
        Meta Class
        """
        model = ProctoredExam

        fields = (
            "id", "course_id", "content_id", "external_id", "exam_name",
            "time_limit_mins", "is_proctored", "is_active"
        )


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User Model.
    """
    id = serializers.IntegerField(required=False)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        """
        Meta Class
        """
        model = User

        fields = (
            "id", "username", "email"
        )


class ProctoredExamStudentAttemptSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProctoredExamStudentAttempt Model.
    """
    proctored_exam_id = serializers.IntegerField(source="proctored_exam_id")
    user_id = serializers.IntegerField(required=False)

    class Meta:
        """
        Meta Class
        """
        model = ProctoredExamStudentAttempt

        fields = (
            "id", "created", "modified", "user_id", "started_at", "completed_at",
            "external_id", "status", "proctored_exam_id", "allowed_time_limit_mins",
            "attempt_code", "is_sample_attempt", "taking_as_proctored"
        )


class ProctoredExamStudentAllowanceSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProctoredExamStudentAllowance Model.
    """
    proctored_exam = ProctoredExamSerializer()
    user = UserSerializer()

    class Meta:
        """
        Meta Class
        """
        model = ProctoredExamStudentAllowance
        fields = (
            "id", "created", "modified", "user", "key", "value", "proctored_exam"
        )
