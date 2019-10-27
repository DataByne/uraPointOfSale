var express = require('express');
var models = require('./models/');
var router = express();

models.sequelize
  .authenticate()
  .then(function () {
    console.log('Connection successful');
  })
  .catch(function(error) {
    console.log("Error creating connection:", error);
  });

router.set('port', process.env.PORT || '3000');

router.get('/api/users', (req, res, next) => {
  return res.json(models.sequelize.User);
});

router.get('*', (req, res, next) => {
  return res.status(500).send('Unknown API endpoint');
});

var server = router.listen(router.get('port'), 'localhost', function() {
  console.log('Running server at http://' + server.address().address + ':' + server.address().port + '/');
});

