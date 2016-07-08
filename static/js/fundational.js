/**
 * Created by haha370104 on 16/7/8.
 */

function getCookie(name) {
    var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");

    if (arr = document.cookie.match(reg))

        return unescape(arr[2]);
    else
        return null;
}

function get_row_html(json, level) {
    var op_html = '<span class="glyphicon glyphicon-pencil my-table-operation-button" aria-hidden="true"\
                                  title="修改"></span>\
                            &nbsp;\
                            <span class="glyphicon glyphicon-remove my-table-operation-button" aria-hidden="true"\
                                  title="删除"></span>';

    level = parseInt(level);
    console.log(json['ID']);
    if (level == 3) {
        html = '<tr><td>' + json['ID'] + '</td><td>' + json['employee_name'] + '</td><td>' + json['f_department'] + '</td><td>' + json['s_department'] + '</td><td>' + json['position_title'] + '</td><td>' + json['position_level'] + '</td><td>' + json['manager_ID'] + '</td><td>' + json['phone'] + '</td><td>' + json['emergency_phone'] + '</td><td>' + json['address'] + '</td><td>' + json['entry_date'] + '</td><td>' + op_html + '</td></tr>'
    } else {
        html = '<tr><td>' + json['ID'] + '</td><td>' + json['employee_name'] + '</td><td>' + json['f_department'] + '</td><td>' + json['s_department'] + '</td><td>' + json['position_title'] + '</td><td>' + json['position_level'] + '</td><td>' + json['manager_ID'] + '</td><td>' + json['phone'] + '</td><td>' + json['emergency_phone'] + '</td><td>' + json['address'] + '</td><td>' + json['entry_date'] + '</td><td></td></tr>'
    }
    return html;
}