import React, {Component} from 'react';
import axios from 'axios';
class signup extends Component{

  constructor(props){
    super(props);
    this.state={
      type: "USER_SIGNUP",
      UserName : "",
      name: "",
      password : ""
    };

    this.hideDisplay={
      display: "none"
    };
    this.showDisplay={
      display: "block"
    };
    this.SignupHandler=this.SignupHandler.bind(this);
    this.showloginForm=this.showloginForm.bind(this);
  }

  SignupHandler(event){
    event.preventDefault();
    console.log(this.state);
    //state here contains the value for submit, great place for validation
    //axios
    document.getElementById("SignUpFeedback").innerHTML="SignUp successful";

    //document.getElementById("SignUpFeedback").innerHTML="USername already taken";


    this.setState({UserName : "", password : "", name: ""});   //clears up the form
  }

  showloginForm(){
    //here button handling
    this.setState({UserName : "", password : "", name: ""});
    document.getElementById("loginForm").style.display="block";
    document.getElementById("signupForm").style.display="none";
    document.getElementById("SignUpFeedback").innerHTML="";


  }



  render() {

    return (
      <div id="signupForm" style={this.hideDisplay}>
        <form onSubmit={this.SignupHandler}>
          <h3>User SignUp</h3>
          <label>UserName</label>
          <input type="text" name="Username"
          onChange={(event)=> this.setState({UserName: event.target.value})}
          value={this.state.UserName}
          required/>
          <br/>
          <label>Your Name</label>
          <input type="text" name="name"
          onChange={(event)=> this.setState({name: event.target.value})}
          value={this.state.name}
          required/>
          <br/>
          <label>Pasword</label>
          <input type="password" name="password"
          onChange={(event)=> this.setState({password: event.target.value})}
          value={this.state.password}
          required />
          <br/>
          <input type="submit" value="SignUp"/>
          <p>Already have a account? Login <input type="button" value="here" onClick={this.showloginForm}/></p>
        </form>
        <div>
          <p id="SignUpFeedback"></p>
        </div>
      </div>
    );
  }

}

export default signup;
