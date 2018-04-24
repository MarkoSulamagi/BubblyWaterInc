import React from 'react';
import { Link } from 'react-router-dom';
import './Navigation.css';
import { Home, File } from 'react-feather';

class Navigation extends React.Component {

    render() {
        return (
            <nav className="col-md-2 d-none d-md-block bg-light sidebar">
                <div className="sidebar-sticky">
                    <ul className="nav flex-column">
                        <li className="nav-item">
                            <Link className="nav-link" to="/">
                                <Home className="feather" />
                                <span data-feather="home"></span>
                                Dashboard <span className="sr-only">(current)</span>
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link" to="/customers">
                                <File className="feather" />
                                Customers
                            </Link>
                        </li>
                    </ul>
                </div>
            </nav>
        );
    }
}

export default Navigation;