from config import app, database_manager
from flask import request
from htmlBuilder.attributes import Class, Style, HtmlTagAttribute, Onclick, Onsubmit, Id, Name
from htmlBuilder.tags import Html, Head, Title, Body, Div, Footer, Ul, Li, Table, Tr, Td, Th, Header, H1, Button, Input, \
    H3, Caption


class Border(HtmlTagAttribute):
    pass


# страница по управлению операторами и мониторингу состояния очереди
@app.route('/operators')
def operators():
    html = Html([],
                Head([],
                     Title([], "FaceQ operators")
                     ),
                H1([], 'Waiting Room'),
                Body([Class('parent'), Style('position: fixed')],
                     Div([Style('display: inline-block; float: left;')],
                         Table([Border('1'), Style('border: 1px solid black; border-collapse: collapse;')],
                               Tr([Style('border: 1px solid black')],
                                  Td([Style('border: 1px solid black')], "Operator ID"),
                                  Td([Style('border: 1px solid black')], "IP Address"),
                                  Td([Style('border: 1px solid black')], "Ticket number"),
                                  Td([Style('border: 1px solid black')], ""),
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
                               ),

                         ),
                     ),
                    Div([Style('display: inline-block; float: left; margin-left: 30px')],
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

                        """)], 'Add operator')),
                Div([Style('display: inline-block; float: left; margin-left: 30px')], f'Queue size: {database_manager.queue_size()}')
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


if __name__ == '__main__':
    app.run()
