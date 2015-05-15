# pinax-{{ app_name }}


!!! note "Pinax Ecosystem"
    This app was developed as part of the Pinax ecosystem but is just a Django app
    and can be used independently of other Pinax apps.
    
    To learn more about Pinax, see <http://pinaxproject.com/>


## Quickstart

Install the development version:

    pip install pinax-{{ app_name }}

Add `pinax-{{ app_name }}` to your `INSTALLED_APPS` setting:

    INSTALLED_APPS = (
        # ...
        "pinax.{{ app_name }}",
        # ...
    )

Add entry to your `urls.py`:

    url(r"^{{ app_name }}/", include("pinax.{{ app_name }}.urls"))
