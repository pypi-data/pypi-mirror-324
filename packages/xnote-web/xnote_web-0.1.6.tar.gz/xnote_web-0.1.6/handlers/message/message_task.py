# encoding=utf-8

import typing
import xutils
import handlers.message.dao as msg_dao

from xutils import Storage
from xnote.core import xtemplate, xauth
from xnote.core.xtemplate import T
from handlers.message.message_utils import list_task_tags
from handlers.message.message_utils import get_tags_from_message_list
from handlers.message.message_utils import is_marked_keyword
from handlers.message.message_utils import sort_keywords_by_marked
from handlers.message.message_model import MessageTag

class TaskListHandler:

    @classmethod
    def hide_side_tags(cls, kw: Storage):
        kw.show_side_tags = False
        kw.message_left_class = "hide"
        kw.message_right_class = "row"
    
    @staticmethod
    def get_task_kw():
        kw = Storage()
        kw.title = T("待办任务")
        kw.html_title = T("待办任务")
        kw.search_type = "task"
        kw.show_back_btn = True
        kw.tag = "task"
        kw.message_placeholder = T("添加待办任务")
        kw.message_tab = "task"
        return kw
    
    @classmethod
    def fix_side_tags(cls, side_tags: typing.List[MessageTag]):
        for tag in side_tags:
            if tag.is_no_tag:
                tag.url = f"/message?tag=task&filterKey=$no_tag"
            else:
                tag.url = f"/message?tag=task&filterKey={xutils.quote(tag.content)}"
    
    @classmethod
    def get_task_create_page(cls):
        show_side_tags = xutils.get_argument_bool("show_side_tags")
        kw = cls.get_task_kw()
        kw.show_input_box = True
        kw.show_system_tag = False
        side_tags = list_task_tags(xauth.current_name())
        cls.fix_side_tags(side_tags)
        kw.side_tag_tab_key = "filterKey"
        kw.side_tags = side_tags
        kw.default_content = xutils.get_argument_str("filterKey")
        kw.search_type = "task"
        kw.search_placeholder = "搜索待办"
        kw.search_ext_dict = dict(tag = "task.search")
        
        if not show_side_tags:
            cls.hide_side_tags(kw)
        
        return xtemplate.render("message/page/task_index.html", **kw)

    @classmethod
    def get_task_by_keyword_page(cls, filter_key):
        return cls.get_task_create_page()

    @classmethod
    def get_task_taglist_page(cls):
        user_name = xauth.current_name()
        msg_list, amount = msg_dao.list_task(user_name, 0, 1000)

        tag_list = get_tags_from_message_list(
            msg_list, "task", display_tag="taglist", search_tag="task")

        for tag in tag_list:
            is_marked = is_marked_keyword(user_name, tag.tag_code)
            tag.set_is_marked(is_marked)

        sort_keywords_by_marked(tag_list)

        kw = cls.get_task_kw()
        kw.date = ""
        kw.tag_list = tag_list
        kw.html_title = T("待办任务")
        kw.message_placeholder = T("添加待办任务")

        kw.show_sub_link = False
        kw.show_task_create_entry = True
        kw.show_task_done_entry = True
        kw.search_type = "task"
        kw.search_ext_dict = dict(tag="task.search")

        return xtemplate.render("message/page/task_tag_index.html", **kw)

    @classmethod
    def get_task_done_page(cls):
        kw = cls.get_task_kw()
        kw.show_system_tag = False
        kw.show_input_box = False
        cls.hide_side_tags(kw)
        return xtemplate.render("message/page/task_done_index.html", **kw)


class TaskTagListPage:

    @xauth.login_required()
    def GET(self):
        return TaskListHandler.get_task_taglist_page()

xurls = (
    r"/message/task/tag_list", TaskTagListPage,
)