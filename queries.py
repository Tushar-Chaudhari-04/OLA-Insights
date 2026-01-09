queries = {

    "successful_bookings": """
        SELECT *
        FROM rides
        WHERE booking_status = 'Success';
    """,

    "avg_ride_distance_by_vehicle": """
        SELECT vehicle_type,
               AVG(ride_distance) AS avg_ride_distance
        FROM rides
        WHERE booking_status = 'Success'
        GROUP BY vehicle_type;
    """,

    "customer_cancellations": """
        SELECT COUNT(*) AS total_canceled_rides_by_customers
        FROM rides
        WHERE booking_status = 'Canceled by Customer';
    """,

    "top_5_customers": """
        SELECT customer_id,
               vehicle_type,
               COUNT(*) AS book_rides_count
        FROM rides
        WHERE booking_status = 'Success'
        GROUP BY customer_id, vehicle_type
        ORDER BY book_rides_count DESC
        LIMIT 5;
    """,

    "driver_cancellations": """
        SELECT COUNT(*) AS canceled_rides_by_drivers
        FROM rides
        WHERE booking_status = 'Canceled by Driver'
          AND canceled_rides_by_driver = 'Personal & Car related issue';
    """,

    "prime_sedan_ratings": """
        SELECT MAX(driver_ratings) AS max_driver_rating,
               MIN(driver_ratings) AS min_driver_rating
        FROM rides
        WHERE vehicle_type = 'Prime Sedan';
    """,

    "upi_payments": """
        SELECT *
        FROM rides
        WHERE payment_method = 'UPI';
    """,

    "avg_customer_rating": """
        SELECT vehicle_type,
               AVG(customer_rating) AS avg_customer_rating
        FROM rides
        GROUP BY vehicle_type;
    """,

    "total_booking_value": """
        SELECT SUM(booking_value) AS total_booking_value
        FROM rides
        WHERE booking_status = 'Success';
    """,

    "incomplete_rides": """
        SELECT booking_id,
               booking_status,
               incomplete_rides_reason
        FROM rides
        WHERE booking_status != 'Success';
    """
}
