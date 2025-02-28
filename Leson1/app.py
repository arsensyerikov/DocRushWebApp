from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Sample news data
news = [
    "Phalane’s Murder Case Postponed: The court has postponed the case involving three men arrested for the murder of a five-year-old, with the next hearing scheduled for August 27​ (SABC News)​.",
    "KZN Police Officers in Trouble: Two police officers in KwaZulu-Natal have been removed from election duties due to misconduct​ (SABC News)​.",
    "IEC Briefs on Special Votes: The IEC is providing updates on the second day of Special Votes, addressing media questions and providing insights into the voting process​ (SABC News)​.",
    "AfriForum’s Appeal Dismissed: AfriForum’s appeal against the “Kill the Boer” song has been dismissed by the Supreme Court of Appeal​ (SABC News)​.",
    "Numsa Pickets Against SA Steel Mills: The National Union of Metalworkers of South Africa (Numsa) is protesting against SA Steel Mills over claims of unfair dismissals​ (SABC News)​.",
    "Nadal Eyes Olympics: After an early exit from the Roland Garros, Rafael Nadal has set his sights on the upcoming Olympics as his main goal​ (SABC News)​.",
    "Sudan Oil Pipeline Resumption: South Sudan officials have announced that the resumption of the Sudan oil pipeline is imminent​ (SABC News)​."
]
city = input("enter your city:")
@app.route("/task", methods=['GET', 'POST'])
def ind():
    if request.method == 'POST':
        
        if city == "Kiev":
            return '24'
        elif city == "Lviv":
            return '21'
        elif city == "Franyk":
            return '22'
        else:
            return 'City not recognized'
    if request.method == 'GET':
        return jsonify({"news": random.choice(news)})

if __name__ == "__main__":
    app.run(debug=True)

# a = input("enter your city:")
# if a == "Kiev":
#     print( '24')
# if a == "Lviv":
#     print('21')
# if a == "Franyk":
#     print('22')