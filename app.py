import os

from config import app, database_manager
from flask import request, send_from_directory, send_file
from htmlBuilder.attributes import Class, Style, HtmlTagAttribute, Onclick, Onsubmit, Id, Name, Src
from htmlBuilder.tags import Html, Head, Title, Body, Div, Footer, Ul, Li, Table, Tr, Td, Th, Header, H1, Button, Input, \
    H3, Caption, Img, Br


class Border(HtmlTagAttribute):
    pass


def create_operators_table():
    return Table([Border('1'), Style('display: inline-block; float: left; margin-left: 30px; '
                                     'border: 1px solid black; border-collapse: collapse;')],
                 Tr([Style('border: 1px solid black')],
                    Td([Style('border: 1px solid black; padding: 10px')], "Operator ID"),
                    Td([Style('border: 1px solid black; padding: 10px')], "IP Address"),
                    Td([Style('border: 1px solid black; padding: 10px')], "Ticket number"),
                    Td([Style('border: 1px solid black; padding: 10px')], ""),
                    ),
                 [
                     Tr([Style('border: 1px solid black')],
                        Td([Style('border: 1px solid black')], str(operator_id)),
                        Td([Style('border: 1px solid black')], str(host)),
                        Td([Style('border: 1px solid black')], str(ticket_number)),
                        Td([Style('border: 1px solid black')],
                           Button([Style('foreground-color: red;'), Onclick(f"""
                       var xmlHttp = new XMLHttpRequest();
                       xmlHttp.onreadystatechange = function() {{ 
                           if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                               window.location.replace("/operators");
                       }}
                       xmlHttp.open("GET", "/delete-operator?id={operator_id}", true);
                       xmlHttp.send(null);
                    """)], 'Delete')),
                        )
                     for operator_id, host, ticket_number in database_manager.select_operators()
                 ]
                 )


def create_add_operator_button():
    return Div([Style('display: inline-block; float: left; margin-left: 30px')],
               Input([Id('host-input'), Name('Add operator')]),
               Button([Onclick("""
                var input = document.getElementById("host-input").value;
                var xmlHttp = new XMLHttpRequest();
                xmlHttp.onreadystatechange = function() {{ 
                    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                        window.location.replace("/operators");
                }}
                xmlHttp.open("GET", "/add-operator?host=" + input, true);
                xmlHttp.send(null);

                """)], 'Add operator'))


def create_queue_size_div():
    return Div([Style('display: inline-block; float: left; margin-left: 30px')],
               f'Queue size: {database_manager.queue_size()}')


def create_diagrams_list():
    return [Img([Src('/download/' + str(day) + '.png')]) for day in range(7)]


# страница по управлению операторами и мониторингу состояния очереди
@app.route('/operators')
def operators():
    html = \
        Html([],
             Head([],
                  Title([], "FaceQ operators")
                  ),
             H1([], 'Waiting Room'),
             Body([Class('parent'), Style('overflow-y: scroll; overflow-x:hidden;')],
                  Div([],
                      create_operators_table(),
                      create_add_operator_button(),
                      create_queue_size_div(),
                      '.'
                      ),
                  Br([]),
                  Div([Style('overflow-y: scroll; overflow-x:hidden;')], create_diagrams_list())
                  )
             )
    return html.render()

    html = Html([],
                Head([],
                     Title([], "FaceQ operators")
                     ),
                H1([], 'Waiting Room'),
                Body([Class('parent'), Style('position: fixed')],
                     Div([],
                         Div([Style('display: inline-block; float: left;')],
                             create_operators_table(),
                             create_add_operator_button(),
                             create_queue_size_div()
                             ),
                         ),

                     ),
                Div([], )

                )
    return html.render()


# удаление оператора из бд
@app.route('/add-operator')
def add_operator():
    host = request.args.get('host')
    if database_manager.add_operator(host):
        return operators()
    else:
        return "Repeated host"


# добавление оператора в бд
@app.route('/delete-operator')
def delete_operator():
    operator_id = request.args.get('id')
    database_manager.delete_by_id(operator_id)
    return operators()


@app.route('/download/<path:filename>')
def download(filename):
    downloads_folder = 'images/' + filename
    return send_file(downloads_folder)


if __name__ == '__main__':
    app.run()
