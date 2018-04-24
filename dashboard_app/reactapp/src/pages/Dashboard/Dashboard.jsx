import React from 'react';
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {loadCustomerCount} from '../../actions/customerActions';
import {loadMeterCount} from '../../actions/meterActions';
import {loadReadingsGraphTotalDailyWaterConsumption} from '../../actions/meterReadingsActions';
import {Line} from 'react-chartjs-2';


class Dashboard extends React.Component {

    componentWillMount = (nextState, replace, callback) => {
        this.graphData = {};

        this.props.dispatch(loadCustomerCount());
        this.props.dispatch(loadMeterCount());
        this.props.dispatch(loadReadingsGraphTotalDailyWaterConsumption());
    };

    componentWillReceiveProps(nextProps) {
        // There's probably a better place and way to do this. Needs better React skills
        // This logic shouldn't be called every time props are received.
        if (Object.keys(nextProps.daily_total_readings_dataset).length !== 0 &&
            nextProps.daily_total_readings_dataset.constructor === Object) {

            let labels = []
            if (Object.keys(nextProps.daily_total_readings_dataset['HOT']).length > 0) {
                labels = Object.keys(nextProps.daily_total_readings_dataset['HOT']);
            } else if (Object.keys(nextProps.daily_total_readings_dataset['COLD']).length > 0) {
                labels = Object.keys(nextProps.daily_total_readings_dataset['COLD']);
            }
            let waterDataset = [];
            let hotWaterDataset = [];
            let coldWaterDataset = [];

            for (let value of labels) {

                hotWaterDataset.push(nextProps.daily_total_readings_dataset['HOT'][value]);
                coldWaterDataset.push(nextProps.daily_total_readings_dataset['COLD'][value]);
                waterDataset.push(nextProps.daily_total_readings_dataset['HOT'][value] +
                    nextProps.daily_total_readings_dataset['COLD'][value]);
            }

            this.graphData = {
                labels: labels,
                datasets: [{
                    label: 'Hot water consumption',
                    data: hotWaterDataset,
                    lineTension: 0,
                    backgroundColor: 'transparent',
                    borderColor: 'red',
                    borderWidth: 4,
                    pointBackgroundColor: 'red'
                },{
                    label: 'Cold water consumption',
                    data: coldWaterDataset,
                    lineTension: 0,
                    backgroundColor: 'transparent',
                    borderColor: '#007bff',
                    borderWidth: 4,
                    pointBackgroundColor: '#007bff'
                },{
                    label: 'Total water consumption',
                    data: waterDataset,
                    lineTension: 0,
                    backgroundColor: 'transparent',
                    borderColor: 'green',
                    borderWidth: 4,
                    pointBackgroundColor: 'green'
                },]
            }
        }
    }

    render() {
        return (
            <main role="main" className="col-md-9 ml-sm-auto col-lg-10 px-4">
                <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                    <h1 className="h2">Dashboard</h1>
                </div>

                <div className="d-flex">
                    <div className="card text-white bg-primary mb-3 col-md-4">
                        <div className="card-body">
                            <h5 className="card-title">{this.props.customer_count} customers</h5>
                        </div>
                    </div>
                    <div className="card text-white bg-secondary mb-3 col-md-4">
                        <div className="card-body">
                            <h5 className="card-title">{this.props.meter_count} meters in total</h5>
                        </div>
                    </div>
                </div>

                <div className="d-flex">
                    <div className="col-md-10">
                        <h4>Total water consumption (daily m3)</h4>
                        <Line data={this.graphData} />
                    </div>
                </div>
            </main>
        );
    }
}

Dashboard.propTypes = {
    customer_count: PropTypes.number.isRequired,
    meter_count: PropTypes.number.isRequired,
    daily_total_readings_dataset: PropTypes.object.isRequired,
};

function mapStateToProps(state, ownProps) {
    return {
        customer_count: state.customer_count,
        meter_count: state.meter_count,
        daily_total_readings_dataset: state.daily_total_readings_dataset
    };
}

export default connect(mapStateToProps)(Dashboard);