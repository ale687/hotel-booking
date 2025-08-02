import pandas as pd

df = pd.read_csv("hotels.csv", dtype={"id": str})
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pd.read_csv("card_security.csv", dtype=str)

class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()
    
    def book(self):
        """Book a hotel by changing its availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check if the hotel is available"""
        avalability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if avalability == "yes":
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object
            
    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here are you booking data:
        Name: {self.customer_name}
        Hotel name: {self.hotel.name}
        """
        return content
     

class CreditCard:
    def __init__(self, number):
        self.number = number
        
    def validate(self, expiration, holder, cvc):
        card_data = {"number": self.number, "expiration": expiration, 
                     "holder": holder, "cvc": cvc}
        if card_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        card_match = df_cards_security[df_cards_security["number"] == self.number]
        if card_match.empty:
            return False  # No se encontró la tarjeta

        password = card_match["password"].values[0]
        return password == given_password

print(df)
hotel_ID = input("Enter hotel ID: ")
hotel = Hotel(hotel_ID)

if hotel.available():
    credit_card = SecureCreditCard(number="1234567890123456")
    if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
        if credit_card.authenticate(given_password="mypass"):
            hotel.book()
            name = input("Enter your names: ")
            reservation_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
            print(reservation_ticket.generate())
        else: 
            print("Authentication failed. Incorrect password.")
    else:
        print("Credit card validation failed.")
else:
    print("Hotel is not available for booking.")