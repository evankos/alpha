import React, { Component } from 'react';
import { connect } from 'react-redux';
// import { ScrollView, Text, TextInput, View, Button } from 'react-native';
import { login } from '../actions';


class Login extends Component {
    constructor (props) {
        super(props);
        this.state = {
            route: 'Login',
            username: '',
            password: ''
        };
    }

    userLogin (e) {
        this.props.onLogin(this.state.username, this.state.password);
        e.preventDefault();
    }

    toggleRoute (e) {
        let alt = (this.state.route === 'Login') ? 'SignUp' : 'Login';
        this.setState({ route: alt });
        e.preventDefault();
    }

    render () {
        let alt = (this.state.route === 'Login') ? 'SignUp' : 'Login';
        return (

            <div className="col-sm-6 col-md-4 col-md-offset-4">
                <h1 className="text-center login-title">Sign in to continue to Bootsnipp</h1>
                <div className="account-wall">
                    <img className="profile-img" src="https://lh5.googleusercontent.com/-b0-k99FZlyE/AAAAAAAAAAI/AAAAAAAAAAA/eu7opA4byxI/photo.jpg?sz=120"
                         alt=""/>
                    <div className="form-signin">
                        <text style={{fontSize: 27}}>{this.state.route}</text>
                        <input type="text" className="form-control" placeholder='Username' required autoFocus={true}
                               value={this.state.username} onChange={(event) => this.setState({ username: event.target.value })}/>
                        <input type="password" className="form-control" placeholder="Password" autoCapitalize='none'
                               autoCorrect={false} value={this.state.password} onChange={(event) => this.setState({ password: event.target.value })}/>
                        <text style={{fontSize: 16, color: 'blue'}} onClick={(e) => this.toggleRoute(e)}>{alt}</text>
                        <button className="btn btn-lg btn-primary btn-block" onClick={(e) => this.userLogin(e)} title={this.state.route}>
                            Sign in</button>
                        {/*<label className="checkbox pull-left">*/}
                        {/*<input type="checkbox" value={this.state.save}/>*/}
                        {/*Remember me*/}
                        {/*</label>*/}
                        <a href="#" className="pull-right need-help">Need help? </a>
                    </div>
                </div>
                <a href="#" className="text-center new-account">Create an account </a>
            </div>

        );
    }
}


const mapStateToProps = (state, ownProps) => {
    return {
        isLoggedIn: state.auth.isLoggedIn
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        onLogin: (username, password) => { dispatch(login(username, password)); },
        onSignUp: (username, password) => { dispatch(signup(username, password)); }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Login);