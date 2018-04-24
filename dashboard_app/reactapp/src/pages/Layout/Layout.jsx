import React from 'react';
import Header from './Header';
import Navigation from './Navigation';
import './Layout.css';

const Layout = ({ children }) => (
    <div>
        <Header />
        <div className="container-fluid">
            <div className="row content-row">
                <Navigation />
                {children}
            </div>
        </div>
    </div>
);

export default Layout;
