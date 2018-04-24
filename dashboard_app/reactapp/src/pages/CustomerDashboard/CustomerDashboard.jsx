import React from 'react';
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {loadCustomer} from '../../actions/customerActions';
import {loadReadingsGraphTotalDailyWaterConsumption} from '../../actions/meterReadingsActions';
import {Line} from 'react-chartjs-2';

class CustomerDashboard extends React.Component {

    componentWillMount = (nextState, replace, callback) => {
        this.graphData = {};

        this.props.dispatch(loadCustomer(this.props.match.params.id));
        this.props.dispatch(loadReadingsGraphTotalDailyWaterConsumption(this.props.match.params.id));
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
                    <h1 className="h2">{this.props.customer.first_name} {this.props.customer.last_name} - {this.props.customer.address}</h1>
                </div>

                <div className="d-flex">
                    <div className="card text-white bg-danger mb-3 col-md-4">
                        <div className="card-body">
                            <h5 className="card-title">{this.props.customer.meters.length} meter(s) in address</h5>
                        </div>
                    </div>
                    <div className="card text-white bg-success mb-3 col-md-4">
                        <div className="card-body">
                            <h5 className="card-title">Battery left in meters:
                                {this.props.customer.meters.map(meter =>
                                    <span key={meter.id}>{meter.last_reading[meter.last_reading.length - 1].battery_percentage}% </span>
                                )}
                            </h5>
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

CustomerDashboard.propTypes = {
    customer: PropTypes.object.isRequired,
    daily_total_readings_dataset: PropTypes.object.isRequired,
};

function mapStateToProps(state, ownProps) {
    return {
        customer: state.customer,
        daily_total_readings_dataset: state.daily_total_readings_dataset
    };
}

export default connect(mapStateToProps)(CustomerDashboard);