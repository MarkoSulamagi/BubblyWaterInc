import React from 'react';
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import CustomerListComponent from '../../components/CustomerList/CustomerList';
import {loadCustomers} from '../../actions/customerActions';

class CustomerList extends React.Component {

    componentWillMount = (nextState, replace, callback) => {
        this.props.dispatch(loadCustomers())
    };

    render() {
        return (
            <main role="main" className="col-md-9 ml-sm-auto col-lg-10 px-4">
                <h2>Customers</h2>
                <div className="table-responsive">
                    <CustomerListComponent customers={this.props.customers} />
                </div>
            </main>
        );
    }
}

CustomerList.propTypes = {
    customers: PropTypes.array.isRequired
};

function mapStateToProps(state, ownProps) {
    return {
        customers: state.customers
    };
}

export default connect(mapStateToProps)(CustomerList);