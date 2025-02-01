# encoding=utf-8
# Created by xupingmao on 2024/09/15
import xutils
from xutils import Storage
from xnote.core import xauth
from xnote.core import xtemplate
from xnote.core import xmanager
from xnote.plugin.table_plugin import BaseTablePlugin
from xnote.plugin import DataTable, TableActionType

class TableExampleHandler(BaseTablePlugin):
    
    title = "表格测试"

    PAGE_HTML = """
{% include test/component/example_nav_tab.html %}

<div class="card">
    <button class="btn" onclick="xnote.table.handleEditForm(this)"
            data-url="?action=edit" data-title="新增记录">新增记录</button>
</div>

<div class="card">
    <div class="card-title">
        <span>表格1-自动宽度</span>
    </div>
    {% include common/table/table.html %}
</div>

<div class="card">
    <div class="card-title">
        <span>表格2-权重宽度</span>
    </div>
    {% set-global xnote_table_var = "weight_table" %}
    {% include common/table/table.html %}
</div>
"""

    def handle_page(self):
        table = DataTable()
        table.add_head("类型", "type", css_class_field="type_class")
        table.add_head("标题", "title", link_field="view_url")
        table.add_head("日期", "date")
        table.add_head("内容", "content")

        table.add_action("编辑", link_field="edit_url", type=TableActionType.edit_form)
        table.add_action("删除", link_field="delete_url", type=TableActionType.confirm, 
                         msg_field="delete_msg", css_class="btn danger")

        row = {}
        row["type"] = "类型1"
        row["title"] = "测试"
        row["type_class"] = "red"
        row["date"] = "2020-01-01"
        row["content"] = "测试内容"
        row["view_url"] = "/note/index"
        row["edit_url"] = "?action=edit"
        row["delete_url"] = "?action=delete"
        row["delete_msg"] = "确认删除记录吗?"
        table.add_row(row)

        kw = Storage()
        kw.table = table
        kw.page = 1
        kw.page_max = 1
        kw.page_url = "?page="

        kw.weight_table = self.get_weight_table()

        return self.response_page(**kw)
    
    def get_weight_table(self):
        table = DataTable()
        table.add_head("权重1", field="value1", width_weight=1)
        table.add_head("权重1", field="value2", width_weight=1)
        table.add_head("权重2", field="value3", width_weight=2)
        table.add_head("权重1", field="value4", width_weight=1)
        table.add_action("编辑", link_field="edit_url", type=TableActionType.edit_form)
        table.add_action("删除", link_field="delete_url", type=TableActionType.confirm, 
                         msg_field="delete_msg", css_class="btn danger")
        
        row = {}
        row["value1"] = "value1"
        row["value2"] = "value2"
        row["value3"] = "value3"
        row["value4"] = "value4"
        row["view_url"] = "/note/index"
        row["edit_url"] = "?action=edit"
        row["delete_url"] = "?action=delete"
        row["delete_msg"] = "确认删除记录吗?"

        table.add_row(row)
        return table


class ExampleHandler:

    def GET(self):
        user_name = xauth.current_name_str()
        xmanager.add_visit_log(user_name, "/test/example")
        
        name = xutils.get_argument_str("name", "")
        if name == "":
            return xtemplate.render("test/page/example_index.html")
        else:
            return xtemplate.render(f"test/page/example_{name}.html")

    def POST(self):
        return self.GET()


xurls = (
    r"/test/example", ExampleHandler,
    r"/test/example/table", TableExampleHandler,
)