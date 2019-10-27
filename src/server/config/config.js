module.exports = {
  development: {
    url: 'postgres://postgres:@localhost:5432/urapos_development',
    dialect: 'postgres'
  },
  testing: {
    url: process.env.DATABASE_URL || 'postgres://postgres:@localhost:5432/urapos_testing',
    dialect: 'postgres'
  },
  stage: {
    url: process.env.DATABASE_URL,
    dialect: 'postgres'
  },
  production: {
    url: process.env.DATABASE_URL,
    dialect: 'postgres'
  }
}

