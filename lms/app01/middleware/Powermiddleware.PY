from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render,redirect,HttpResponse


class Powermiddleware(MiddlewareMixin):
    can_pass = ['/','/log_out','/login','/sign_in','/log_out/','/login/','/sign_in/','/img_upload/']
    def process_request(self, request):
        print(request.path)
        try:
            print(request.session['user'])
        except:
            pass
        if '/MEDIA/pic/' in request.path:
            return
        if 'user' not in request.session:
            if request.path not in self.can_pass:
                return redirect("/")
            else:
                return None
        else:
            print("0.0.0.0.0.")
            if not request.session['user']['is_admin']:
                print("!!!!!!@1111111@@@@")
                if "admin" in request.path :
                    print("0.0.0.0.0.")
                    return HttpResponse(status = 403)
                else:
                    if request.path == "/":
                        return redirect("/book_list/")
            else:
                print("!!!!!!@@@@@")
                if 'admin' not in request.path  and  "book_rest" not in request.path and request.path not in self.can_pass:
                    return HttpResponse(status = 400)
                
            
