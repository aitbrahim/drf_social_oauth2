import six


class UserMixin(object):
    ACCESS_TOKEN_EXPIRED_THRESHOLD = 5
    user = ''
    provider = ''
    uid = None
    extra_data = None

    def set_extra_data(self, extra_data=None):
        if extra_data and self.extra_data != extra_data:
            if self.extra_data and not isinstance(
                    self.extra_data, six.string_types):
                self.extra_data.update(extra_data)
            else:
                self.extra_data = extra_data
            return True
