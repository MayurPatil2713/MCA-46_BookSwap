
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash
)
import re
from database import get_db, init_db

app = Flask(__name__)

app.secret_key = "bookswap-dev-key-change-before-deployment"

init_db()


@app.route("/")
def index():
    # Read search and filter values from the URL
    search = request.args.get("q", "").strip()
    semester = request.args.get("semester", "")
    condition = request.args.get("condition", "")
    status = request.args.get("status", "")

    # Start with a query that can accept optional conditions
    sql = "SELECT * FROM books WHERE 1=1"
    params = []

    # Search in the title or subject
    if search:
        sql += " AND (title LIKE ? OR subject LIKE ?)"
        keyword = f"%{search}%"
        params.extend([keyword, keyword])

    # Validate filter values before using them
    if semester in {"1", "2", "3", "4"}:
        sql += " AND semester = ?"
        params.append(int(semester))

    if condition in {"New", "Good", "Fair"}:
        sql += " AND book_condition = ?"
        params.append(condition)

    if status in {"Available", "Sold"}:
        sql += " AND status = ?"
        params.append(status)

    sql += " ORDER BY listed_on DESC, book_id DESC"

    conn = get_db()

    try:
        rows = conn.execute(sql, params).fetchall()
        books = [dict(row) for row in rows]

        available_count = conn.execute(
            "SELECT COUNT(*) FROM books WHERE status = 'Available'"
        ).fetchone()[0]

        sold_count = conn.execute(
            "SELECT COUNT(*) FROM books WHERE status = 'Sold'"
        ).fetchone()[0]

        average_price = conn.execute(
            "SELECT AVG(selling_price) FROM books"
        ).fetchone()[0] or 0

    finally:
        conn.close()

    return render_template(
        "index.html",
        books=books,
        search=search,
        semester=semester,
        condition=condition,
        status=status,
        available_count=available_count,
        sold_count=sold_count,
        average_price=average_price
    )

@app.route("/add", methods=["POST"])
def add_book():
    # Read and clean the submitted form data
    title = request.form.get("title", "").strip()
    subject = request.form.get("subject", "").strip()
    semester = request.form.get("semester", "")
    condition = request.form.get("book_condition", "")
    mrp_text = request.form.get("mrp", "").strip()
    price_text = request.form.get("selling_price", "").strip()
    seller = request.form.get("seller_name", "").strip()
    mobile = request.form.get("seller_mobile", "").strip()

    errors = []

    # Validate text fields
    if not 3 <= len(title) <= 80:
        errors.append("Title must contain 3 to 80 characters.")

    if not subject:
        errors.append("Subject is required.")

    if semester not in {"1", "2", "3", "4"}:
        errors.append("Please select a valid semester.")

    if condition not in {"New", "Good", "Fair"}:
        errors.append("Please select a valid book condition.")

    if not seller:
        errors.append("Seller name is required.")

    if not re.fullmatch(r"[0-9]{10}", mobile):
        errors.append("Mobile number must contain exactly 10 digits.")

    # Validate prices and handle empty or non-numeric input
    try:
        mrp = float(mrp_text)
        if mrp <= 0:
            errors.append("MRP must be greater than zero.")
    except ValueError:
        mrp = 0
        errors.append("Enter a valid numeric MRP.")

    try:
        selling_price = float(price_text)
        if selling_price <= 0:
            errors.append("Selling price must be greater than zero.")
    except ValueError:
        selling_price = 0
        errors.append("Enter a valid numeric selling price.")

    if mrp > 0 and selling_price > mrp:
        errors.append("Selling price cannot exceed MRP.")

    # Reject invalid data before touching the database
    if errors:
        for error in errors:
            flash(error, "danger")
        return redirect(url_for("index"))

    # Insert the validated record
    conn = get_db()

    try:
        conn.execute(
            """
            INSERT INTO books (
                title, subject, semester, book_condition,
                mrp, selling_price, seller_name, seller_mobile,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Available')
            """,
            (
                title, subject, int(semester), condition,
                mrp, selling_price, seller, mobile
            )
        )
        conn.commit()
        flash("Book listed successfully!", "success")

    except Exception:
        conn.rollback()
        flash("Could not save the book. Please try again.", "danger")

    finally:
        conn.close()

    return redirect(url_for("index"))


@app.route("/sell/<int:book_id>", methods=["POST"])
def sell_book(book_id):
    conn = get_db()

    try:
        cursor = conn.execute(
            """
            UPDATE books
            SET status = 'Sold'
            WHERE book_id = ? AND status = 'Available'
            """,
            (book_id,)
        )
        conn.commit()

        if cursor.rowcount == 1:
            flash("Book marked as Sold.", "success")
        else:
            flash("Book not found or already sold.", "warning")

    except Exception:
        conn.rollback()
        flash("Could not update the book status.", "danger")

    finally:
        conn.close()

    return redirect(url_for("index"))




if __name__ == "__main__":
    app.run(debug=True)
