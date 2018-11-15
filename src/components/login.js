import React, {Component} from 'react';
import axios from 'axios';
class login extends Component{

  constructor(props){
    super(props);
    this.state={
      type: "USER_LOGIN",
      UserName : "",
      password : ""
    };

    this.hideDisplay={
      display: "none"
    };
    this.showDisplay={
      display: "block"
    };

    this.LoginHandler=this.LoginHandler.bind(this);
  }


  LoginHandler(event){
    event.preventDefault();
    console.log(this.state);

    var para = document.createElement("P");                       // Create a <p> element
    var t = document.createTextNode("You are logged in");      // Create a text node
    para.appendChild(t);                                          // Append the text to <p>
    document.getElementById("loginFeedback").appendChild(para);           // Append <p> to <div>
    //state here contains the value for submit, great place for validation
    //axios
  }

  showSignUpForm(){
    //here button handling
    document.getElementById("loginForm").style.display="none";
    document.getElementById("signupForm").style.display="block";
  }

  render() {
    return (
      <div id="loginForm">
        <form onSubmit={this.LoginHandler}>
          <h3>User Login</h3>
          <label>UserName</label>
          <input type="text" name="Username"
          onChange={(event)=> this.setState({UserName: event.target.value})}
          value={this.state.UserName}
          required/>
          <br/>
          <label>Password</label>
          <input type="password" name="password"
          onChange={(event)=> this.setState({password: event.target.value})}
          value={this.state.password}
          required />
          <br/>
          <input type="submit" value="login"/>
          <p>Don't have a account? SignUp <input type="button" value="here" onClick={this.showSignUpForm}/></p>
        </form>
        <div id="loginFeedback">
        </div>
      </div>
    );
  }
}

export default login;
