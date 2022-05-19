from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from . import google_2fa, google_2fa_encrypt, google_2fa_helpers
import time

# Create your views here.
def path(request, path):
    if path == "2fa":
        print("\n\n REQUEST 2fa \n\n")
        time.sleep(1)
        secrets = google_2fa.get_secrets()
        valid_time = google_2fa.get_valid_time()
        return render(request, "app/app.html", {
            "secrets": secrets,
            "valid_time": valid_time
        })
    elif path == "script":
        print("\n\n REQUEST script \n\n")
        secrets = google_2fa_helpers.parse_add_button_text(request.POST["query_param"])
        for i, (k,v) in enumerate(secrets.items()):
            #print("{} - {}".format(k, v))
            google_2fa.sqlite3_db_add(google_2fa_encrypt.encode(k, google_2fa.PASSWORD), google_2fa_encrypt.encode(v, google_2fa.PASSWORD))
        return render(request, "app/app.html")
    else:
        return HttpResponseNotFound("Page not found!")