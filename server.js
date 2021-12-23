const express = require('express')
const app = express()
const port = 4000

app.get('/', (req, res) => {
  res.redirect('/index.html')
})

const SCHEDULE_DATABASE = {
  "revision": 600,
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

app.use(express.json())

function processSync(syncData, db) {
  const { type, requestId } = syncData;
  if (type !== "sync") {
    throw `Error: invalid type ${type}`;
  }
  if (isNaN(requestId)) {  // Should be positive integer.
    throw "Error: missing or invalid request ID";
  }

  const storeResults = {};
  [ "events", "resources" ].forEach(storeName => {
    const dbStore = db[storeName];
    if (syncData[storeName]) {
      const { added, removed, updated } = syncData[storeName];
      const results = {};
      if (added) {
        added.forEach((a) => {
          const newRecord = Object.assign({ id: dbStore.nextId }, a);
          dbStore.rows.push(newRecord)
          dbStore.nextId += 1;
          if (!results.rows) results.rows = []
          results.rows.push(newRecord);
        })
      }
      if (updated) {
        updated.forEach((u) => {
          const { id } = u;
          const updatedRecord = dbStore.rows.find(ele => ele.id == id);
          if (!updatedRecord) {
            throw `Error: update id ${id} not found`;
          }
          Object.assign(updatedRecord, u)
          if (!results.rows) results.rows = []
          results.rows.push(updatedRecord);
        })
      }
      if (removed) {
        removed.forEach((r) => {
          const { id } = r;
          const index = dbStore.rows.findIndex(ele => ele.id == id);
          if (index < 0) {
            throw `Error: remove id ${id} not found`;
          }
          dbStore.rows.splice(index, 1)
          if (!results.removed) results.removed = []
          results.removed.push({ id });
        })
      }
      if (results.rows || results.removed) {
        storeResults[storeName] = results;
      }
    }
  });

  db.revision += 1;
  const { revision } = db;
  return Object.assign({ success: true, revision, requestId }, storeResults)
}

app.post('/sync/schedule.json', (req, res) => {
  const requestData = req.body;
  console.log("REQUEST", JSON.stringify(requestData, 4));
  const responseData = processSync(req.body, SCHEDULE_DATABASE);
  console.log("RESPONSE", JSON.stringify(responseData, 4));
  res.json(responseData)
});

app.get('/data/schedule.json', (req, res) => {
  res.json({
    success: true,
    resources: {
      rows: SCHEDULE_DATABASE.resources.rows
    },
    events: {
      "rows": SCHEDULE_DATABASE.events.rows
    }
  })
})

app.get('/data/plan.json', (req, res) => {
  res.json({
    "success": true,
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
        ]
    },
    "events": {
        "rows": [
            { "resourceId": 1, "startDate": "2021-12-05", "duration": 7, "durationUnit": "day", "eventColor": "blue" },
            { "resourceId": 2, "startDate": "2021-12-04", "duration" : 7, "durationUnit" : "day", "eventColor": "blue"},
            { "resourceId": 3, "startDate": "2021-12-03", "duration" : 7, "durationUnit" : "day", "eventColor": "blue"},
            { "resourceId": 4, "startDate": "2021-11-25", "duration" : 7, "durationUnit" : "day", "eventColor": "orange"},
            { "resourceId": 5, "startDate": "2021-11-25", "duration" : 7, "durationUnit" : "day", "eventColor": "orange"},
            { "resourceId": 6, "startDate": "2021-11-25", "duration" : 7, "durationUnit" : "day", "eventColor": "orange"},
            { "resourceId": 7, "startDate": "2021-11-26", "duration" : 7, "durationUnit" : "day", "eventColor": "purple"},
            { "resourceId": 8, "startDate": "2021-11-26", "duration" : 7, "durationUnit" : "day", "eventColor": "purple"},
            { "resourceId": 9, "startDate": "2021-11-26", "duration" : 7, "durationUnit" : "day", "eventColor": "purple"},
            { "resourceId": 10, "startDate": "2021-11-27", "duration": 7, "durationUnit": "day", "eventColor": "red"},
            { "resourceId": 11, "startDate": "2021-11-27", "duration": 7, "durationUnit": "day", "eventColor": "red"},
            { "resourceId": 12, "startDate": "2021-11-27", "duration": 7, "durationUnit": "day", "eventColor": "red"}
        ]
    }
  });
})

app.use(express.static("."))

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
