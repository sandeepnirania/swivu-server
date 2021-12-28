const { Sequelize } = require("sequelize");

const SCHEDULE_DATABASE = {
  "resources": {
      "rows": [
          { "id": 1, "assignee": "Jimbo", "name": "Jimbo", "assignment": "Copley Group" },
          { "id": 2, "assignee": "Mike Kostka", "name": "Mike Kostka", "assignment": "Pfizer" },
          { "id": 3, "assignee": "Edmar", "name": "Edmar", "assignment": "Barkan" },
          { "id": 4, "assignee": "Joe Sapienza", "name": "Joe Sapienza", "assignment": "Harvard" },
          { "id": 5, "assignee": "Jon Drohan", "name": "Jon Drohan", "assignment": "Weston Associates" },
          { "id": 6, "assignee": "Muru", "name": "Muru", "assignment": "Paradigm" },
          { "id": 7, "assignee": "Dave Lannan", "name": "Dave Lannan", "assignment": "Quirk" },
          { "id": 8, "assignee": "Dave Russell", "name": "Dave Russell", "assignment": "Equity" },
          { "id": 9, "assignee": "Ben Brown", "name": "Ben Brown", "assignment": "Thayer" },
          { "id": 10, "assignee": "Joe Fraser", "name": "Joe Fraser", "assignment": "Boston College" },
          { "id": 11, "assignee": "Mike Simonson", "name": "Mike Simonson", "assignment": "Diana" },
          { "id": 12, "assignee": "Mike Somadelis", "name": "Mike Somadelis", "assignment": "Erland" }
      ],
      nextId: 13 
  },
  "events": {
      "rows": [
          { id: 1, "resourceId": 1, "startDate": "2021-12-05", "duration": 7, "durationUnit": "day", "eventColor": "blue" },
          { id: 2, "resourceId": 2, "startDate": "2021-12-04", "duration" : 7, "durationUnit" : "day", "eventColor": "blue"},
          { id: 3, "resourceId": 3, "startDate": "2021-12-03", "duration" : 7, "durationUnit" : "day", "eventColor": "blue"},
          { id: 4, "resourceId": 4, "startDate": "2021-12-05", "duration" : 7, "durationUnit" : "day", "eventColor": "orange"},
          { id: 5, "resourceId": 5, "startDate": "2021-12-05", "duration" : 7, "durationUnit" : "day", "eventColor": "orange"},
          { id: 6, "resourceId": 6, "startDate": "2021-12-05", "duration" : 7, "durationUnit" : "day", "eventColor": "orange"},
          { id: 7, "resourceId": 7, "startDate": "2021-12-06", "duration" : 7, "durationUnit" : "day", "eventColor": "purple"},
          { id: 8, "resourceId": 8, "startDate": "2021-12-06", "duration" : 7, "durationUnit" : "day", "eventColor": "purple"},
          { id: 9, "resourceId": 9, "startDate": "2021-12-06", "duration" : 7, "durationUnit" : "day", "eventColor": "purple"},
          { id: 10, "resourceId": 10, "startDate": "2021-12-07", "duration": 7, "durationUnit": "day", "eventColor": "red"},
          { id: 11, "resourceId": 11, "startDate": "2021-12-07", "duration": 7, "durationUnit": "day", "eventColor": "red"},
          { id: 12, "resourceId": 12, "startDate": "2021-12-07", "duration": 7, "durationUnit": "day", "eventColor": "red"}
      ],
      nextId: 13
  }
};

async function seed() {
  const connection = new Sequelize("postgres://localhost:5432/swivu-server");
  let exitStatus = 0;

  try {
    await connection.authenticate()
    await connection.close();
  }
  catch (error) {
    console.error("ERROR", error);
    exitStatus = 1;
  }
  process.exit(exitStatus);
}

seed();
