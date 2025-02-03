import os
import shutil

from os.path import join, exists
from bomiot.cmd.copyfile import copy_files
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.parsers import MultiPartParser, FormParser
from functools import reduce

from .serializers import UserSerializer, FileSerializer
from .filter import UserFilter, FileFilter
from.page import CorePageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Permission, Files
from .message import permission_message_return, detail_message_return, msg_message_return, others_message_return

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.conf import settings

User = get_user_model()


class UserPage(CorePageNumberPagination):

    def get_permission_return_data(self, data) -> dict:
        return { "label": permission_message_return(self.request.META.get('HTTP_LANGUAGE', ''), data.name), "value": data.name }

    def query_data_add(self) -> list:
        permission_list = Permission.objects.all()
        permission_data_list = list(map(lambda data: self.get_permission_return_data(data), permission_list))
        return [
            ("permission", permission_data_list)
        ]


class UserList(viewsets.ModelViewSet):
    """
        list:
            Response a user data list（all）
    """
    pagination_class = UserPage
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "username", "created_time", "updated_time", ]
    filter_class = UserFilter

    def get_queryset(self):
        if self.request.user:
            return User.objects.filter(is_delete=False)
        else:
            return User.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return UserSerializer
        else:
            return self.http_method_not_allowed(request=self.request)


class PermissionList(viewsets.ModelViewSet):
    """
        list:
            Response a permission data list（all）
    """
    queryset = Permission.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]


class UserCreate(viewsets.ModelViewSet):
    """
        create:
            create a user
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = UserFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return UserSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, **kwargs):
        data = self.request.data
        user_check = User.objects.filter(username=data.get('username'), is_delete=False)
        if user_check.exists():
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "User exists"))
        else:
            if self.request.auth.is_superuser is True:
                User.objects.create_user(username=data.get('username'), password=data.get('username'))
                user_folder = join(settings.MEDIA_ROOT, data.get('username'))
                exists(user_folder) or os.makedirs(user_folder)
            else:
                if "Set Permission For User" not in self.request.auth.permission:
                    raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                             "User does not have permission to create user"))
                else:
                    User.objects.create_user(username=data.get('username'), password=data.get('username'))
                    user_folder = join(settings.MEDIA_ROOT, data.get('username'))
                    exists(user_folder) or os.makedirs(user_folder)
        return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                               "Success Create User"), status=200)


class UserPermission(viewsets.ModelViewSet):
    """
        create:
            Set permission for user
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = UserFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return UserSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def get_permission_data(self, data):
        permission_data = Permission.objects.filter(name=data).first()
        return {
            permission_data.name: permission_data.api
        }

    def create(self, request, **kwargs):
        data = self.request.data
        user_check = User.objects.filter(id=data.get('id'), is_delete=False)
        if user_check.exists() is False:
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "User not exists"))
        else:
            user_data = user_check.first()
            if "Set Permission For User" not in self.request.auth.permission:
                raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                         "User does not have permission to set permission for user"))
            else:
                if self.request.auth.id == int(data.get('id')):
                    raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                             "Can not change your own permission"))
                else:
                    if user_data.is_superuser is True:
                        raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                                 "Can not change admin's permission"))
                    else:
                        permission_list = data.get('permission')
                        data_list = list(map(lambda data: self.get_permission_data(data), permission_list))
                        permission_data = reduce(lambda x, y: {**x, **y}, data_list)
                        user_data.permission = permission_data
                        user_data.save()
            return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                               "Success Change User Permission"), status=200)


class UserChangePWD(viewsets.ModelViewSet):
    """
        create:
            Change Password
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = UserFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return UserSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, **kwargs):
        data = self.request.data
        user_check = User.objects.filter(id=data.get('id'), is_delete=False)
        if user_check.exists() is False:
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "User not exists"))
        else:
            user_data = user_check.first()
            if self.request.auth.is_superuser is True:
                user_data.set_password(str(data.get('pwd')))
                user_data.save()
            else:
                if "Change Password" not in self.request.auth.permission:
                    raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                             "User does not have permission to change password"))
                else:
                    if self.request.auth.id == int(data.get('id')):
                        user_data.set_password(str(data.get('pwd')))
                        user_data.save()
                    else:
                        raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                                 "User can only change your own password"))
            return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                               "Success Change Password"), status=200)


class UserLock(viewsets.ModelViewSet):
    """
        create:
            Lock one User
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = UserFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return UserSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, **kwargs):
        data = self.request.data
        user_check = User.objects.filter(id=data.get('id'), is_delete=False)
        if user_check.exists() is False:
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "User not exists"))
        else:
            user_data = user_check.first()
            if user_data.is_superuser:
                raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                         "Can not lock admin"))
            else:
                if "Lock & Unlock User" not in self.request.auth.permission:
                    raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                             "User does not have permission to lock user"))
                else:
                    if self.request.auth.id == int(data.get('id')):
                        raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                                 "User can not lock/unlock your own"))
                    else:
                        if user_data.is_active is True:
                            user_data.is_active = False
                            user_data.save()
                            return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                               "Success lock User"), status=200)
                        else:
                            user_data.is_active = True
                            user_data.save()
                            return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                               "Success unlock User"), status=200)


class UserDelete(viewsets.ModelViewSet):
    """
        create:
            Delete one User
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = UserFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return UserSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, **kwargs):
        data = self.request.data
        user_check = User.objects.filter(id=data.get('id'), is_delete=False)
        if user_check.exists() is False:
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "User not exists"))
        else:
            user_data = user_check.first()
            if user_data.is_superuser:
                raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                         "Can not delete admin"))
            else:
                if "Delete One User" not in self.request.auth.permission:
                    raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                             "User does not have permission to delete user"))
                else:
                    if self.request.auth.id == int(data.get('id')):
                        raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                                 "User can not delete your own"))
                    else:
                        user_data.is_delete = True
                        return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                           "Success delete User"), status=200)


class UserUpload(viewsets.ModelViewSet):
    """
        create:
            upload files
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = FileFilter
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        if self.request.user:
            return Files.objects.filter(Q(owner=self.request.auth.username, is_delete=False) | Q(shared=True, is_delete=False))
        else:
            return Files.objects.none()

    def get_serializer_class(self):
        if self.action in ['create']:
            return FileSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, *args, **kwargs):
        data = self.request.FILES
        for file_name in data:
            file_obj = self.request.FILES.get(file_name)
            file_data = file_obj.read()
            file_path = join(join(settings.MEDIA_ROOT, str(self.request.auth.username)), file_obj.name)
            with open(file_path, 'wb') as f:
                f.write(file_data)
            f.close()
            context = {}
            msg = others_message_return(self.request.META.get('HTTP_LANGUAGE', ''),  "Success upload files")
            context['msg'] = f"{msg} {file_obj.name}"
            return Response(context, status=200)