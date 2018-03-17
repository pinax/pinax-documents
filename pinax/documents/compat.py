try:
    # Python 2
    from itertools import izip_longest
except ImportError:
    # Python 3
    from itertools import zip_longest as izip_longest  # noqa

try:
    from account.mixins import LoginRequiredMixin
except ImportError:
    from django.contrib.auth.mixins import LoginRequiredMixin  # noqa
