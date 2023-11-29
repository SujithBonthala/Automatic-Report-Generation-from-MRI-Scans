const express = require("express")
const cors = require("cors")
const app = express()
const fileUpload = require('express-fileupload');
const fs = require ('fs');
app.use(express.json())
app.use(express.urlencoded({ extended: true }))
app.use(cors())

app.use(fileUpload({
    createParentPath : true
}))

app.post("/upload", (req, res) => {
    
	if(req.files === null)
	{
		res.status(400).json({ msg: "No file was uploaded" });
	}

	// var folder = `${__dirname}/client_react/public/uploads/`;
	
	const file = req.files.file;
	const fileName = file.name;
	const file_path = `${__dirname}/scans/${fileName}`;
	try
	{
		file.mv(file_path, err => {
			if(err)
			{
				console.error(err);
				return res.status(500).send(err);
			}
			
			res.json({ fileName: fileName, filePath: file_path });
		});
	}
	catch(err)
	{
		console.error(err);
		return res.status(500).send(err);
	}
});


app.listen(5000, ()=>{
    console.log("Port is running at 5000!");
})