db.interactions.createIndex({ customer_id: 1, timestamp: -1 });
db.devices.createIndex({ customer_id: 1, device_id: 1 }, { unique: true });
