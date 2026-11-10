# What I Learned

While working on this assignment, I learned how the product quantity affects a packing recommendation. The dimensions and weight saved for a product describe one item. If an order has several of that item, the application checks that many copies and adds their weights together. That can make a larger box necessary, even though the individual product dimensions stay the same.

I created Django project which uses models to store products, boxes, orders, and order items from what i have learned and by using some help of AI.Here the migration command creates the database tables, and the seed command adds example catalog data. The Django admin page is useful for changing product and box information without editing the application code. And by using the Django admin page we can update the items from the ecommerce website.

The packing logic considers whether the products fit inside a box, whether their combined weight is within its limit, and the box cost. A small box is not chosen just because an order has a small number of items, the actual dimensions and weight matter. The project uses a packing technique of how the quantity affects the dimensions and this dimensions affect the finalized box size, so I learned that a recommendation can depend on the method used to test arrangements and that the result should be verified with test cases.

AI helped generate and revise much of the application. I ran the setup commands, tried the order form, checked how quantities affected recommendations, and ran the Django tests. That showed me why it is useful to test the application with real inputs instead of assuming the code works just because it starts.
