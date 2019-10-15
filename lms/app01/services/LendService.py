from app01.services import BookService,UserService
from app01 import models
from django.db import transaction
import traceback
from django.forms.models import model_to_dict
from datetime import *

class LendService:
    def __init__(self):
        self.us = UserService.UserService()
        self.bs = BookService.BookService()
        self.bss = models.BookState.objects
        self.obj = models.UserToBook.objects

    
    def query_lend(self,uid):
        try:
            result_set = self.obj.filter(uid=uid)
            has_down_result = []
            not_down_result = []
            for i in result_set:
                print(i.bid)
                book = self.bs.query_book_by_id(i.bid)[0]
                bookstate = self.bss.get(bsid=i.bsid,uid=uid)
                mdict = model_to_dict(bookstate)
                mdict['bid'] = i.bid
                i = bookstate
                mdict['lend_time'] = i.lend_time.strftime("%Y-%m-%d %H:%M:%S")
                mdict['is_overtime'] = False
                if datetime.now() > i.lend_time + timedelta(hours=mdict['should_back_time']):
                    mdict['is_overtime'] = True
                mdict['should_back_time'] = (i.lend_time + timedelta(hours=mdict['should_back_time'])).strftime("%Y-%m-%d %H:%M:%S")
                mdict['book'] = book
                if mdict['down'] == 1:
                    mdict['back_time'] = mdict['back_time'].strftime("%Y-%m-%d %H:%M:%S")
                    has_down_result.append(mdict)
                else:
                    not_down_result.append(mdict)
            return [has_down_result,not_down_result]
        except:
            traceback.print_exc()
            return False
    
    def lend_book(self,bid,uid):
        try:
            book_detail = self.obj.filter(uid = uid)
            if self.bs.obj.get(bid = bid).can_lend <= 0:
                raise
            if len(book_detail) >= 3:
                count = 0
                for i in book_detail:
                    if self.bss.get(bsid = i.bsid,uid=uid).down == 0:
                        count += 1
                        if count >= 3:
                            raise
            
            with transaction.atomic():
                a = self.bss.create(
                    uid = uid,
                    down = 0
                    )
                self.obj.create(
                    bsid = a.bsid,
                    uid = uid,
                    bid = bid
                )
                self.bs.lend_book(bid=bid)
            return True
        except:
            traceback.print_exc()
            return False
        
    def back_book(self,bsid,uid):
        try:
            with transaction.atomic():
                obj = self.bss.filter(bsid=bsid,uid=uid)
                bid = self.obj.get(bsid=bsid,uid=uid).bid
                obj.update(back_time=datetime.now(),down=1)
                can_lend = self.bs.obj.get(bid=bid).can_lend
                self.bs.obj.filter(bid=bid).update(can_lend=can_lend+1)
                obj = self.bss.get(bsid = bsid,uid=uid)
                result = model_to_dict(obj)
                result['lend_time'] = obj.lend_time.strftime("%Y-%m-%d %H:%M:%S")
                result['should_back_time'] = (obj.lend_time + timedelta(hours=result['should_back_time'])).strftime("%Y-%m-%d %H:%M:%S")
                result['back_time'] = result['back_time'].strftime("%Y-%m-%d %H:%M:%S")
                result['book'] = self.bs.query_book_by_id(bid)[0]
            return result
        except:
            traceback.print_exc()
            return False

    def pay_book(self,bsid,uid):
        try:
            with transaction.atomic():
                obj = self.bss.filter(bsid=bsid,uid=uid)
                bid = self.obj.get(bsid=bsid,uid=uid).bid
                obj.update(back_time=datetime.now(),down=1,beizhu="丢失赔偿")
                number = self.bs.obj.get(bid=bid).number
                self.bs.obj.filter(bid=bid).update(number=number-1)
                obj = self.bss.get(bsid = bsid,uid=uid)
                result = model_to_dict(obj)
                result['lend_time'] = obj.lend_time.strftime("%Y-%m-%d %H:%M:%S")
                result['should_back_time'] = (obj.lend_time + timedelta(hours=result['should_back_time'])).strftime("%Y-%m-%d %H:%M:%S")
                result['back_time'] = result['back_time'].strftime("%Y-%m-%d %H:%M:%S")
                result['book'] = self.bs.query_book_by_id(bid)[0]
            return result
        except:
            traceback.print_exc()
            return False

    def continue_lend(self,bsid,uid):
        try:
            obj = self.bss.get(bsid=bsid,uid=uid)
            should_back_time = obj.should_back_time
            lend_time = obj.lend_time
            self.bss.filter(bsid=bsid,uid=uid).update(should_back_time = should_back_time + 168)
            result = (lend_time + timedelta(hours=should_back_time + 168)).strftime("%Y-%m-%d %H:%M:%S")
            return result
        except Exception as e:
            return False