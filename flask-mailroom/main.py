import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donor, Donation

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/create/', methods=['GET', 'POST'])
def create_donation():
    if request.method == 'POST':
        donation_amount = request.form['donation_amount']
        donor_name = request.form['donor_name']

        try:
            donor = Donor.select().where(Donor.name == donor_name).get()
        except Donor.DoesNotExist:
            donor = Donor(name=donor_name)
            donor.save()

        donation = Donation(value=donation_amount, donor=donor)
        donation.save()
        return redirect('/donations/')
    return render_template('create.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

