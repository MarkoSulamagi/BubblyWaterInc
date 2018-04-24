import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';

const CustomerListComponent = ({customers}) => {

    return (
        <table className="table table-striped table-sm">
            <thead>
            <tr>
                <th>#</th>
                <th>Name</th>
                <th>Address</th>
                <th>Meters in household</th>
            </tr>
            </thead>
            <tbody>
            {customers.map(customer =>
                <tr key={customer.id}>
                    <td>{customer.id}</td>
                    <td><Link to={`/customers/${customer.id}`}>{customer.first_name} {customer.last_name}</Link></td>
                    <td>{customer.address}</td>
                    <td>{customer.meters.length}</td>
                </tr>
            )}
            </tbody>
        </table>
    );
};

CustomerListComponent.propTypes = {
    customers: PropTypes.array.isRequired
};

export default CustomerListComponent;