from http.server import HTTPServer, BaseHTTPRequestHandler
from restaurantDatabase import RestaurantDatabase
import cgi

class RestaurantPortalHandler(BaseHTTPRequestHandler):
    
    def __init__(self, *args):
        self.database = RestaurantDatabase()
        BaseHTTPRequestHandler.__init__(self, *args)
    
    def do_POST(self):
        try:
            if self.path == '/addReservation':
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                customer_name = form.getvalue("customer_name")
                contact_info = form.getvalue("contact_info")
                reservation_time = form.getvalue("reservation_time")
                number_of_guests = form.getvalue("number_of_guests")
                special_requests = form.getvalue("special_requests")

                
                if not customer_name or not contact_info or not reservation_time or not number_of_guests.isdigit():
                    self.send_error(400, "Invalid input data")
                    return
                
                number_of_guests = int(number_of_guests)
                
                
                self.database.addReservation(customer_name, contact_info, reservation_time, number_of_guests, special_requests)
                print("Reservation added for customer:", customer_name)
                
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                self.wfile.write(b"""
                                    <html>
                                    <head>
                                    <title>Add Reservation</title>
                                    </head>
                                    <body>
                                    <center>
                                    <h2>Reservation Added</h2>
                                    <p>Reservation added successfully .</p>
                                    <a href='/addReservation'>Add Another Reservation</a><br>
                                    
                                    <a href='/viewReservations'>View Reservations</a>
                                    </center>
                                    </body>
                                    </html>
                                 """)   
                
            elif self.path == '/deleteReservation':
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                reservation_id = form.getvalue("reservation_id")

                
                if not reservation_id or not reservation_id.isdigit():
                    self.send_error(400, "Invalid reservation ID")
                    return

                reservation_id = int(reservation_id)

                
                self.database.deleteReservation(reservation_id)
                print("Reservation deleted with ID:", reservation_id)

                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                self.wfile.write(b"""
                                <html>
                                <head>
                                <title>Delete Reservation</title>
                                </head>
                                <body>
                                <center>
                                <h2>Reservation Deleted</h2>
                                <p>Reservation has been successfully deleted.</p>
                                <a href='/deleteReservation'>Delete Another Reservation</a><br>
                                <a href='/viewReservations'>View Reservations</a>
                                </center>
                                </body>
                                </html>
                                  """)

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

        return
    
    def do_GET(self):
        
        try:
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"""
                                 <html><head><title>Restaurant Portal</title></head>
                                 <body>
                                 <center>
                                 <h1>Welcome to Mastors Restaurant Portal</h1>
                                 <hr>
                
                                 <div> <a href='/'>Home</a>| \
                                 <a href='/addReservation'>Add Reservation</a>|\
                                 <a href='/deleteReservation'>Delete Reservation</a>|\
                                 <a href='/viewReservations'>View Reservations</a></div>
                                 <hr><h2>All Reservations</h2>
                                 <table border=2> \
                                 <tr><th> Reservation ID </th>\
                                 <th> Customer Name </th>\
                                 <th> Contact Info </th>\
                                 <th> Reservation Time </th>\
                                 <th> Number of Guests </th>\
                                 <th> Special Requests </th></tr>
                                  """)
                records = self.database.getAllReservations()
                for row in records:
                    self.wfile.write(b' <tr> <td>')
                    self.wfile.write(str(row[0]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[1]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[2]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[3]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[4]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[5]).encode())
                    self.wfile.write(b'</td></tr>')
                
                self.wfile.write(b"</table></center>")
                self.wfile.write(b"</body></html>")
                return

            elif self.path == '/addReservation':
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                self.wfile.write(b"""
                                <html>
                                 <head>
                                  <title> Add Reservation </title>
                                 </head>
                                 <body>
                                 <center><h2>Add Reservation</h2>
                                 <form method='post' action='/addReservation'>
                                 <label>Customer Name: </label>
                                 <input type='text' name='customer_name' required><br>
                                 <label>Contact Info: </label>
                                 <input type='text' name='contact_info' required><br>
                                 <label>Reservation Time: </label>
                                 <input type='text' name='reservation_time' required><br>
                                 <label>Number of Guests: </label>
                                 <input type='text' name='number_of_guests' required><br>
                                 <label>Special Requests: </label>
                                 <input type='text' name='special_requests'><br>
                                 <input type='submit' value='Submit'>
                                </form>
                                </center>
                                </body>
                                </html>
                                """)
                        
                return

            elif self.path == '/deleteReservation':
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                self.wfile.write(b"""
                                 <html><head><title>Delete Reservation</title></head>
                                 <body>
                                 <center><h2>Delete Reservation</h2>
                                 <form method='post' action='/deleteReservation'>
                                 <label>Reservation ID to delete: </label>
                                 <input type='text' name='reservation_id' required><br>
                                 <input type='submit' value='Delete'>
                                 </form>
                                 </center></body></html>
                                 """)

                return

            elif self.path == '/viewReservations':
                reservations = self.database.getAllReservations()
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                self.wfile.write(b"""
                                 <html><head><title>View Reservations</title></head>
                                 <body>
                                 <center><h1>View Reservations</h1>
                                 <hr>
                                 <div> <a href='/'>Home</a>| \
                                 <a href='/addReservation'>Add Reservation</a>|\
                                 <a href='/deleteReservation'>Delete Reservation</a>|\
                                 <a href='/viewReservations'>View Reservations</a></div>
                                <hr><h2>All Reservations</h2>
                                <table border=1>
                                <tr>
                                <th>Reservation ID</th>
                                <th>Customer Name</th>
                                <th>Contact Info</th>
                                <th>Reservation Time</th>
                                <th>Number of Guests</th>
                                <th>Special Requests</th>
                                </tr>
                                """)
                
                for row in reservations:
                    self.wfile.write(b"<tr>")
                    for item in row:
                        self.wfile.write(b"<td>")
                        self.wfile.write(str(item).encode())
                        self.wfile.write(b"</td>")
                    self.wfile.write(b"</tr>")
                    
                self.wfile.write(b"</table>")
                self.wfile.write(b"</center></body></html>")
                return
            
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

def run(server_class=HTTPServer, handler_class=RestaurantPortalHandler, port=8000):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port {}'.format(port))
    httpd.serve_forever()

run()
