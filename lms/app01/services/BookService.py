from django.forms.models import model_to_dict
from django.db import transaction
from app01 import models
import traceback

class BookService: 
    def __init__(self):
        self.ts = models.BookType.objects
        self.tbs = models.TypeToBook.objects
        self.obj = models.Book.objects
        self.bss = models.BookState.objects

    def add_book(self,isbn_id,b_type,img_path,name,publisher,auther,price,descri):
        try:
            with transaction.atomic():
                self.obj.create(
                    isbn_id = isbn_id,
                    b_type = b_type,
                    img_path = img_path,
                    name = name,
                    publisher = publisher,
                    auther = auther,
                    price = price,
                    number = 2,
                    descri = descri
                )
                bid = model_to_dict(self.obj.get(isbn_id = isbn_id))['bid']
                if len(self.ts.filter(name = b_type)) == 0:
                    self.ts.create(
                        name = b_type
                    )
                
                tid = model_to_dict(self.ts.get(name = b_type))['tid']
                self.tbs.create(
                    bid = bid,
                    tid = tid
                )
            return True
        except:
            traceback.print_exc()
            return False

    def add_book_num(self,bid):
        try:
            with transaction.atomic():
                result_set = self.obj.get(bid = bid)
                num = model_to_dict(result_set)['number']
                can_lend = model_to_dict(result_set)['can_lend']
                self.obj.filter(bid=bid).update(number=num+1,can_lend=can_lend+1)
            return True
        except:
            return False


    def update_book_msg(self,bid,name,isbn_id,b_type,auther,publisher,price,img_path):
        try:
            with transaction.atomic():
                result_set = self.obj.filter(bid=bid).update(
                    name=name,
                    isbn_id=isbn_id,
                    b_type=b_type,
                    auther=auther,
                    publisher=publisher,
                    price=price,
                    img_path=img_path
                )
                if b_type != model_to_dict(self.obj.get(bid=bid))['name']:
                    if len(self.ts.filter(name = b_type)) == 0:
                        self.ts.create(
                            name = b_type
                        )
                        tid = model_to_dict(self.ts.get(name = b_type))['tid']
                        self.tbs.create(
                            tid = tid,
                            bid = bid
                        )
                    else:
                        tid = model_to_dict(self.ts.get(name = b_type))['tid']
                        self.tbs.filter(bid = bid).update(
                            tid = tid
                        )
                else:
                    result_set = self.obj.filter(bid=bid).update(
                            name=name,
                            isbn_id=isbn_id,
                            auther=auther,
                            publisher=publisher,
                            price=price,
                            img_path=img_path
                        )
            return True
        except:
            traceback.print_exc()
            return False
    
    def delete_book(self,bid):
        try:
            with transaction.atomic():
                self.obj.filter(bid = bid).delete()
                self.tbs.filter(bid = bid).delete()
            return True
        except:
            return False
    
    def sub_book(self,bid,lend_id = None):
        try:
            with transaction.atomic():
                num = model_to_dict(self.obj.get(bid=bid))['number']
                can_lend = model_to_dict(self.obj.get(bid=bid))['can_lend']
                if can_lend > 0:
                    if num - 1 <= 0 :
                        return False
                    else:
                        self.obj.filter(bid = bid).update(number=num-1,can_lend=can_lend-1)
                        return True
                else:
                    return "id"
            
        except:
            traceback.print_exc()
            return False

    def remove_book(self,bid):
        try:
            with transaction.atomic():
                if self.bss.filter(bid=bid):
                    self.bss.filter(bid=bid).update(down = 1)
                self.obj.filter(bid=bid).delete()
                self.tbs.filter(bid=bid).delete()
            return True
        except:
            return False


    def lend_book(self,bid):
        book_num = self.obj.get(bid = bid).can_lend
        print(book_num)
        self.obj.filter(bid = bid).update(can_lend = book_num - 1)











    def length(self):
        return len(self.obj.all())

    def all_book(self):
        result = []
        for i in self.obj.all():
            result.append(model_to_dict(i))
        return result

    def query_type_book(self,btype):
        if type(btype) != int:
            try:
                obj = models.BookType.objects.get(name=btype)
                btype = obj.tid
            except:
                return False

        try:
            result_set = self.tbs.filter(tid=btype)
            result = []
            for i in result_set:
                bid = model_to_dict(i)['bid']
                result.append(model_to_dict(self.obj.get(bid=bid)))
            return result
        except:
            return False

    def all_type(self):
        try:
            result_set = self.ts.all()
            result = []
            for i in result_set:
                result.append(model_to_dict(i))
            return result
        except:
            return False

    def query_book_by_id(self,bid):
        try:
            bid = int(bid)
            result_set = self.obj.get(bid = bid)
            return [model_to_dict(result_set)]
        except:
            return False

    def query_book_by_name(self,name):
        try:
            result_set = self.obj.filter(name__contains = name)
            result = []
            for i in result_set:
                result.append(model_to_dict(i))
            return result
        except:
            return False

    def query_book_by_auth(self,auther):
        try:
            result_set = self.obj.filter(auther__contains = auther)
            result = []
            for i in result_set:
                result.append(model_to_dict(i))
            return result
        except:
            traceback.print_exc()
            return False

    def query_book_by_pub(self,pub):
        try:
            result_set = self.obj.filter(publisher__contains = pub)
            result = []
            for i in result_set:
                result.append(model_to_dict(i))
            return result
        except:
            traceback.print_exc()
            return False

    def query_book_by_type(self,type_name):
        try:

            result_set = self.obj.all(type = type_name)
            result = []
            for i in result_set: 
                result.append(model_to_dict(i))
            return result
        except:
            return False
        
    def query_all(self,start,end):
        try:
            result_set = self.obj.all()[start:end]
            result = []
            for i in result_set:
                result.append(model_to_dict(i))
            return result
        except:
            traceback.print_exc()
            return False


    def query_all_type(self):
        try:
            result_set = self.obj.values_list("b_type")
            result = []
            for i in result_set:
                if i[0] not in result:
                    result.append(i[0])
            return result
        except:
            return False

    def query_book_by_isbn_id(self,isbn_id):
        try:
            result_set = self.obj.filter(isbn_id = isbn_id)
            result = []
            for i in result_set: 
                result.append(model_to_dict(i))
            return result
        except:
            traceback.print_exc()
            return False


    

    