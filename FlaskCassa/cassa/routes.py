from sqlalchemy import desc, text

from cassa import app, db
from flask import render_template, redirect, url_for, flash
from cassa.model import Item, User, Receipt, ReceiptsItems
from cassa.forms import LoginForm, RegisterForm, PurchaseForm, NewReceiptForm
from flask_login import login_user
from datetime import datetime


@app.route('/', methods=['GET', 'POST'])
def home_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(matricola=form.matricola.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            return redirect(url_for('cashier_page'))
        else:
            flash('MATRICOLA O PASSWORD NON CORRETTI', category='danger')
    return render_template('home.html', form=form)


@app.route('/prodotti')
def products_page():
    items = Item.query.all()
    return render_template('prodotti.html', items=items)


@app.route('/registrazione', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(matricola=form.matricola.data,
                              password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"Errore nella creazione dell'utenza: {err_msg}", category='danger')
    return render_template('registrazione.html', form=form)


@app.route('/cassa', methods=['GET', 'POST'])
def cashier_page():
    purchase_form = PurchaseForm()
    new_receipt_form = NewReceiptForm()
    date = datetime.now()
    items_purchased = []
    if new_receipt_form.validate_on_submit():
        new_receipt = Receipt()
        db.session.add(new_receipt)
        db.session.commit()
    if Item.query.filter_by(barcode=purchase_form.barcode.data).first() is not None:
        item_purchased = Item.query.filter_by(barcode=purchase_form.barcode.data).first()
        if Receipt.query.order_by(desc('id')).first() != {}:
            receipts_items = ReceiptsItems(receipt=Receipt.query.order_by(desc(text('id'))).first().id,
                                           item=item_purchased.id)
            db.session.add(receipts_items)
            db.session.commit()
        else:
            receipt = Receipt()
            db.session.add(receipt)
            db.session.commit()
            receipts_items = ReceiptsItems(receipt=receipt,
                                           item=item_purchased.id)
            db.session.add(receipts_items)
            db.session.commit()
        receipt = Receipt.query.order_by(desc(text('id'))).first()
        items_id = db.session.query(ReceiptsItems.item).filter_by(receipt=receipt.id)
        items_purchased = Item.query.filter(Item.id.in_(items_id))


    return render_template('cassa.html', datetime=date, purchase_form=purchase_form, items_purchased=items_purchased, new_receipt_form=new_receipt_form)
