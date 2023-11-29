const mongoose=require("mongoose")
mongoose.connect("mongodb://localhost:27017/login-report-generation-mri-scans")
.then(()=>{
    console.log("MongoDB is connected");
})
.catch(()=>{
    console.log('MongoDB connection failed');
})


const loginSchema = new mongoose.Schema({
    name:{
        type:String,
        required:true
    },
    age:{
        type:String,
        required:true
    },
    gender:{
        type:String,
        required:true
    },
    email:{
        type:String,
        required:true
    },
    password:{
        type:String,
        required:true
    }

})

const collection = mongoose.model("Login Details", loginSchema)

module.exports = collection