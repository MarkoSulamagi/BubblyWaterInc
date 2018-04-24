import React from 'react';
import logo from './logo.svg';
import { Link } from 'react-router-dom';
import './Header.css';

class Header extends React.Component {

  render() {
    return (
        <nav className="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow">
            <Link className="navbar-brand col-sm-3 col-md-2 mr-0" to="/">
                <img src={logo} alt="Bubbly Water Inc" className="logo" /> Bubbly Water Inc
            </Link>
        </nav>
    );
  }
}

export default Header;
