const express = require('express')
const path = require('path')
const fs = require('fs')
const {Router} = require('express')

const app = express()
const docsRouter = Router()

app.use(express.static(path.join(__dirname, 'build')))

app.get('*', function (req, res, next) {
        res.sendFile(path.join(__dirname, 'build', 'index.html'))
    }
)

const PORT = process.env.NODE_PORT || 9000
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server is running on port ${PORT}...`)
})