import React from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux';
import { BrowserRouter, Switch, Route, Redirect } from 'react-router-dom';
import registerServiceWorker from './registerServiceWorker';
import Dashboard from './pages/Dashboard/Dashboard';
import CustomerList from './pages/CustomerList/CustomerList';
import CustomerDashboard from './pages/CustomerDashboard/CustomerDashboard';
import configureStore from './store/configureStore';
import 'bootstrap/dist/css/bootstrap.min.css';
import Layout from './pages/Layout/Layout';

const store = configureStore();

render(
    <Provider store={store}>
        <BrowserRouter>
            <Layout>
                <Switch>
                    <Route exact path="/" render={() => <Redirect to="/dashboard" />} />
                    <Route path="/dashboard" component={Dashboard} />
                    <Route path="/customers/:id" component={CustomerDashboard} />
                    <Route path="/customers" component={CustomerList} />
                </Switch>
            </Layout>
        </BrowserRouter>
    </Provider>,
    document.getElementById('root')
);

registerServiceWorker();
