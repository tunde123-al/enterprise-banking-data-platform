// MongoDB Digital Banking Interactions Collection Setup
db = db.getSiblingDB('digital_banking');

db.createCollection('customer_interactions');

db.customer_interactions.createIndex({ "customer_id": 1 });
db.customer_interactions.createIndex({ "interaction_timestamp": -1 });
db.customer_interactions.createIndex({ "channel": 1 });
db.customer_interactions.createIndex({ "category": 1 });

print("MongoDB digital_banking initialized successfully.");
