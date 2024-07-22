from tkinter import Tk, Label, Entry, Button, messagebox, Frame
from PIL import Image, ImageTk
import hashlib
import random
import tkinter.filedialog as filedialog

class FlightReservationSystem:
    def __init__(self):
        self.users = {}
        self.user_index = {}  # Dictionary for indexing
        self.flights = {
            'ABC123': {'source': 'New York', 'destination': 'Los Angeles', 'departure_time': '2023-05-25 09:00 AM', 'arrival_time': '2023-05-25 12:00 PM', 'available_seats': 100, 'price': 200},
            'DEF456': {'source': 'Chicago', 'destination': 'Miami', 'departure_time': '2023-05-26 08:30 AM', 'arrival_time': '2023-05-26 11:30 AM', 'available_seats': 150, 'price': 150},
            'GHI789': {'source': 'San Francisco', 'destination': 'Seattle', 'departure_time': '2023-05-27 10:00 AM', 'arrival_time': '2023-05-27 12:30 PM', 'available_seats': 120, 'price': 180}
        }
        self.bookings = {}

    def register_user(self, name, age):
        user_id = self.generate_user_id()
        user_hash = hashlib.sha256(str(user_id).encode()).hexdigest()
        self.users[user_id] = {'name': name, 'age': age, 'hash': user_hash}
        self.user_index[user_hash] = user_id  # Add index entry
        return user_id

    def search_flight(self, flight_number):
        if flight_number in self.flights:
            return self.flights[flight_number]
        return None

    def book_flight(self, flight_number, user_id, seats):
        if flight_number in self.flights:
            flight = self.flights[flight_number]
        if flight_number not in self.bookings:
            self.bookings[flight_number] = {}

        available_seats = flight.get('available_seats', 0)

        if available_seats >= seats:
            flight['available_seats'] = available_seats - seats

            ticket_number = self.generate_ticket_number(flight_number)
            self.bookings[flight_number][ticket_number] = {'user_id': user_id, 'seats': seats}
            
            # Update user_index dictionary with the ticket_number
            self.user_index[ticket_number] = flight_number
            
            return ticket_number
        else:
            return None
        return None


    def cancel_flight(self, flight_number, ticket_number):
        if flight_number in self.bookings and ticket_number in self.bookings[flight_number]:
            flight = self.flights[flight_number]
            seats_to_cancel = self.bookings[flight_number][ticket_number]['seats']
            flight['available_seats'] += seats_to_cancel

            self.bookings[flight_number].pop(ticket_number)
            return True
        return False

    def generate_ticket_number(self, flight_number):
        if flight_number in self.bookings:
            num_bookings = len(self.bookings[flight_number])
        else:
            num_bookings = 0

        ticket_number = f"{flight_number}-{num_bookings + 1}"
        return ticket_number

    def generate_user_id(self):
        user_id = random.randint(10, 99)
        while user_id in self.users:
            user_id = random.randint(10, 99)
        return str(user_id)

    def get_user_info_from_ticket(self, ticket_number):
        for flight_number, tickets in self.bookings.items():
            for ticket, info in tickets.items():
                if ticket == ticket_number:
                    user_id = info['user_id']
                    flight_info = self.flights[flight_number]
                    user_info = self.users[user_id]
                    return {
                        'user_name': user_info['name'],
                        'ticket_number': ticket,
                        'flight_number': flight_number,
                        'source': flight_info['source'],
                        'destination': flight_info['destination'],
                        'price': flight_info['price']
                    }
        return None

class RegistrationPanel:
    def __init__(self, root, reservation_system):
        self.root = root
        self.reservation_system = reservation_system

        self.name_label = Label(self.root, text="Name:")
        self.name_label.pack()
        self.name_entry = Entry(self.root)
        self.name_entry.pack()

        self.age_label = Label(self.root, text="Age:")
        self.age_label.pack()
        self.age_entry = Entry(self.root)
        self.age_entry.pack()

        self.register_button = Button(self.root, text="Register", command=self.register_user)
        self.register_button.pack()

    def register_user(self):
        name = self.name_entry.get()
        age = self.age_entry.get()

        if name and age:
            user_id = self.reservation_system.register_user(name, age)
            messagebox.showinfo("Registration Successful", f"User Registered!\nUser ID: {user_id}")
        else:
            messagebox.showerror("Registration Failed", "Please enter a valid Name and Age.")


class FlightSearchPanel:
    def __init__(self, root, reservation_system):
        self.root = root
        self.reservation_system = reservation_system

        self.flight_label = Label(self.root, text="Enter Flight Number:")
        self.flight_label.pack()
        self.flight_entry = Entry(self.root)
        self.flight_entry.pack()

        self.search_button = Button(self.root, text="Search Flight", command=self.search_flight)
        self.search_button.pack()

        self.result_label = Label(self.root, text="")
        self.result_label.pack()

    def search_flight(self):
        flight_number = self.flight_entry.get()
        flight_info = self.reservation_system.search_flight(flight_number)
        if flight_info:
            message = f"Flight Found:\nFlight Number: {flight_number}\nSource: {flight_info['source']}\nDestination: {flight_info['destination']}\nDeparture Time: {flight_info['departure_time']}\nArrival Time: {flight_info['arrival_time']}\nPrice: ${flight_info['price']}"
            messagebox.showinfo("Flight Information", message)
        else:
            messagebox.showinfo("Flight Not Found", "Flight Not Found")

class TicketBookingPanel:
    def __init__(self, root, reservation_system):
        self.root = root
        self.reservation_system = reservation_system

        self.flight_label = Label(self.root, text="Enter Flight Number:")
        self.flight_label.pack()
        self.flight_entry = Entry(self.root)
        self.flight_entry.pack()

        self.user_id_label = Label(self.root, text="User ID:")
        self.user_id_label.pack()
        self.user_id_entry = Entry(self.root)
        self.user_id_entry.pack()

        self.seats_label = Label(self.root, text="No. of Seats:")
        self.seats_label.pack()
        self.seats_entry = Entry(self.root)
        self.seats_entry.pack()

        self.book_button = Button(self.root, text="Book Ticket", command=self.book_ticket)
        self.book_button.pack()

        self.ticket_label = Label(self.root, text="")
        self.ticket_label.pack()

        self.display_button = Button(self.root, text="Display User Info", command=self.display_information)
        self.display_button.pack()

        self.save_button = Button(self.root, text="Save Information", command=self.save_information)
        self.save_button.pack()


    def book_ticket(self):
        flight_number = self.flight_entry.get()
        user_id = self.user_id_entry.get()
        seats = self.seats_entry.get()

        if flight_number and user_id and seats:
            if user_id not in self.reservation_system.users:
                messagebox.showerror("Booking Failed", "Invalid User ID. Please register first.")
            else:
                ticket_number = self.reservation_system.book_flight(flight_number, user_id, int(seats))
                if ticket_number:
                    messagebox.showinfo("Booking Successful", f"Ticket booked successfully!\nTicket Number: {ticket_number}")
                    self.ticket_label.config(text=f"Ticket Number: {ticket_number}")
                else:
                    messagebox.showerror("Booking Failed", "Booking failed. Please check the flight number or available seats.")
        else:
            messagebox.showerror("Booking Failed", "Please enter valid Flight Number, User ID, and No. of Seats.")

    def display_information(self):
            ticket_number = self.ticket_label.cget("text").split(": ")[1]
            information = self.reservation_system.get_user_info_from_ticket(ticket_number)

            if information:
              messagebox.showinfo("Ticket Information", f"User Name: {information['user_name']}\nTicket Number: {information['ticket_number']}\nFlight Number: {information['flight_number']}\nSource: {information['source']}\nDestination: {information['destination']}\nPrice: {information['price']}")
            else:
              messagebox.showerror("Ticket Information", "Invalid Ticket Number. Please check and try again.")

    def save_user_info(self, message):
        with open("text.txt", "a") as file:
            file.write(message + "\n\n")
    def save_information(self):
        ticket_number = self.ticket_label.cget("text").split(": ")[1]
        information = self.reservation_system.get_user_info_from_ticket(ticket_number)

        if information:
            filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if filename:
                with open(filename, 'w') as file:
                    file.write(f"User Name: {information['user_name']}\n")
                    file.write(f"Ticket Number: {information['ticket_number']}\n")
                    file.write(f"Flight Number: {information['flight_number']}\n")
                    file.write(f"Source: {information['source']}\n")
                    file.write(f"Destination: {information['destination']}\n")
                    file.write(f"Price: {information['price']}\n")

class FlightCancellationPanel:
    def __init__(self, root, reservation_system):
        self.root = root
        self.reservation_system = reservation_system

        self.flight_label = Label(self.root, text="Enter Flight Number:")
        self.flight_label.pack()
        self.flight_entry = Entry(self.root)
        self.flight_entry.pack()

        self.ticket_label = Label(self.root, text="Enter Ticket Number:")
        self.ticket_label.pack()
        self.ticket_entry = Entry(self.root)
        self.ticket_entry.pack()

        self.cancel_button = Button(self.root, text="Cancel Ticket", command=self.cancel_ticket)
        self.cancel_button.pack()

        

    def cancel_ticket(self):
        flight_number = self.flight_entry.get()
        ticket_number = self.ticket_entry.get()

        if flight_number and ticket_number:
            if self.reservation_system.cancel_flight(flight_number, ticket_number):
                messagebox.showinfo("Cancellation Successful", "Ticket canceled successfully!")
            else:
                messagebox.showerror("Cancellation Failed", "Invalid Flight Number or Ticket Number. Please check and try again.")
        else:
            messagebox.showerror("Cancellation Failed", "Please enter valid Flight Number and Ticket Number.")


class FlightReservationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Reservation System")

        # Load flight image
        self.bg_image = Image.open("flight_image.jpg")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create background label
        self.background_label = Label(root, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create frames
        self.registration_frame = Frame(root, bg="white", padx=100, pady=50)
        self.registration_frame.pack()

        self.flight_search_frame = Frame(root, bg="white", padx=100, pady=20)
        self.flight_search_frame.pack()

        self.ticket_booking_frame = Frame(root, bg="white", padx=100, pady=20)
        self.ticket_booking_frame.pack()

        self.flight_cancellation_frame = Frame(root, bg="white", padx=100, pady=50)
        self.flight_cancellation_frame.pack()

        # Create reservation system
        self.reservation_system = FlightReservationSystem()

        # Create panels
        self.registration_panel = RegistrationPanel(self.registration_frame, self.reservation_system)
        self.flight_search_panel = FlightSearchPanel(self.flight_search_frame, self.reservation_system)
        self.ticket_booking_panel = TicketBookingPanel(self.ticket_booking_frame, self.reservation_system)
        self.flight_cancellation_panel = FlightCancellationPanel(self.flight_cancellation_frame, self.reservation_system)


if __name__ == "__main__":
    root = Tk()
    app = FlightReservationApp(root)
    root.mainloop()
