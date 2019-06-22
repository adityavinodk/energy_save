import React, { Component } from 'react';
import Response from '../../layout/Response';
import headers from '../../utils/Headers';

class WashingMachine extends Component {
  constructor() {
    super();
    // order_of_training_data = ['ApplStandard', 'Brand', 'Cap', 'CEC Cold', 'CEC_', 'Cold Water Cons', 'Combination', 'Conn_Mode', 'Country', 'delayStartMode', 'Depth', 'DetergentType', 'Height', 'internal_heater', 'powerConsMode', 'Prog Name', 'standbyPowerUsage', 'Type', 'Width', 'Program Time']    // specifications = ['AS/NZS 2040.2:2005', 'WHIRLPOOL', 7, 150, 400, 100, True, 'Dual', 'India', True, 565, 'Non Drum', 850, 'No', 0.4, 'normal', 0.45, 'Drum', 600, 120]
    // specifications = ['AS/NZS 2040.2:2005', 'WHIRLPOOL', 7, 150, 400, 100, True, 'Dual', 'India', True, 565, 'Non Drum', 850, 'No', 0.4, 'normal', 0.45, 'Drum', 600, 120]
    this.state = {
        'applStandard':'AS/NZS 2040.2:2005',
        'brand':'',
        'cap':'',
        'cecCold':'',
        'cecWarm':'',
        'coldWaterCons':'',
        'combination':true,
        'connMode':'Dual',
        'country':'',
        'delayStartMode':true,
        'depth':'',
        'detergentType':'Non Drum',
        'height':'',
        'internalHeater':'Yes',
        'powerConsMode':'',
        'progName':'',
        'standbyPowerUsage':'',
        'type':'Drum',
        'width':'',
        'progTime':'',
        'response':'',
        'loading':false
    }
    this.handleChange = this.handleChange.bind(this);
    this.submitForm = this.submitForm.bind(this);
    this.handleBoolean = this.handleBoolean.bind(this);
  }
  handleChange(event) {
    event.preventDefault();
    this.setState({ [event.target.name] : event.target.value });
  }
  handleBoolean(event){
    event.preventDefault();
    var value, combination = event.target.name;
    if(combination === 'true'){
      value = true;
    }
    else value = false;
    this.setState({[event.target.name]: value});
  }
  submitForm(e) {
    e.preventDefault();
    this.setState({'loading': true});
    const data = [
        this.state.applStandard,
        this.state.brand,
        parseInt(this.state.cap),
        parseInt(this.state.cecCold),
        parseInt(this.state.cecWarm),
        parseInt(this.state.coldWaterCons),
        this.state.combination,
        this.state.connMode,
        this.state.country,
        this.state.delayStartMode,
        parseInt(this.state.depth),
        this.state.detergentType,
        parseInt(this.state.height),
        this.state.internalHeater,
        parseFloat(this.state.powerConsMode),
        this.state.progName,
        parseFloat(this.state.standbyPowerUsage),
        this.state.type,
        parseInt(this.state.width),
        parseInt(this.state.progTime)
    ];
    // console.log(data);
    fetch('http://localhost:5000/api/predict/washing_machine', {
      method: 'POST',
      mode: 'cors',
      cache: 'no-cache',
      credentials: 'same-origin',
      headers: headers,
      redirect: 'follow',
      referrer: 'no-referrer',
      body: JSON.stringify({
        "specifications": data
      }),
    })
      .then(response => response.json())
      .then(res => {
        console.log(res);
        this.setState({'response':{
          'category' : res.category,
          'info': res.info,
          'inference': res.inference
        }})
      })
  }

  render() {
    var content;
    const formContent = (
      <div>
        <div className="container-fluid mb-5 display-4">
          Washing Machine Details
        </div>
        <form className="container w-50">

            <div className="form-group">
                <label className="form-inline">Appliance Standard</label>
                <select
                className="form-control"
                name='applStandard'
                value={this.state.applStandard}
                onChange={this.handleChange}
                >
                <option value="AS/NZS 2040.2:2005">AS/NZS 2040.2:2005</option>
                <option value="AS/NZS 2040.2:2005 (Legacy)">AS/NZS 2040.2:2005 (Legacy)</option>
                <option value="AS/NZS 2040.2:2000 (Legacy)">AS/NZS 2040.2:2000 (Legacy)</option>
                <option value="Greenhouse and Energy Minimum Standards (Clothes Washing Machines) Determination 2015">Greenhouse and Energy Minimum Standards (Clothes Washing Machines) Determination 2015</option>
                <option value="Greenhouse and Energy Minimum Standards (Clothes Washing Machines) Determination 2012">Greenhouse and Energy Minimum Standards (Clothes Washing Machines) Determination 2012</option>
                </select>
            </div>
            
            <div className="form-group">
                <label className="form-inline">Brand</label>
                <input
                type='text'
                className="form-control"
                placeholder='Name of the Brand'
                name='brand'
                value={this.state.brand}
                onChange={this.handleChange}
                />
            </div>

            <div className="form-group">
                <label className="form-inline">Capacity</label>
                <input
                type='number'
                className="form-control"
                placeholder='Enter value in kg'
                name='cap'
                value={this.state.cap}
                onChange={this.handleChange}
                />
            </div>

            <div className="form-group">
                <label className='form-inline'>Current Comparitive Energy Consumption for Cold Use</label>
                <input
                type='number'
                className="form-control"
                placeholder='Energy Consumption of the product expressed as kilowatt hours per years'
                name="cecCold"
                value={this.state.cecCold}
                onChange={this.handleChange}
                />
            </div>

            <div className="form-group">
                <label className='form-inline'>Current Comparitive Energy Consumption for Warm Use</label>
                <input
                type='number'
                className="form-control"
                placeholder='Energy Consumption of the product expressed as kilowatt hours per years'
                name="cecWarm"
                value={this.state.cecWarm}
                onChange={this.handleChange}
                />
            </div>

            <div className="form-group">
                <label className='form-inline'>Cold Water Consumption</label>
                <input
                type='number'
                className="form-control"
                placeholder='Average cold water consumption in whole litres'
                name="coldWaterCons"
                value={this.state.coldWaterCons}
                onChange={this.handleChange}
                />
            </div>

            <div className="form-group">
                <label className="form-inline">Combination - washer+dryer?</label>
                <select
                className="form-control"
                name='combination'
                value={this.state.combination}
                onChange={this.handleBoolean}
                >
                <option value="true">True</option>
                <option value="false">False</option>
                </select>
            </div>

            <div className="form-group">
                <label className="form-inline">Connection Mode</label>
                <select
                className="form-control"
                name='connMode'
                value={this.state.connMode}
                onChange={this.handleChange}
                >
                <option value="Dual">Dual</option>
                <option value="Cold">Cold</option>
                </select>
            </div>

            <div className="form-group">
                <label className="form-inline">Country</label>
                <input
                type='text'
                className="form-control"
                placeholder='Country of Manufacture'
                name='country'
                value={this.state.country}
                onChange={this.handleChange}
                />
            </div>

            <div className="form-group">
                <label className="form-inline">Delay Start Mode</label>
                <select
                className="form-control"
                name='delayStartMode'
                value={this.state.delayStartMode}
                onChange={this.handleBoolean}
                >
                <option value="true">True</option>
                <option value="false">False</option>
                </select>
            </div>

            <div className="form-group">
                <label className="form-inline">Depth</label>
                <input
                type='number'
                className="form-control"
                placeholder='Depth in mm'
                name='depth'
                value={this.state.depth}
                onChange={this.handleChange}
                />
            </div>

            <div className="form-group">
                <label className="form-inline">Detergent Type</label>
                <select
                className="form-control"
                name='detergentType'
                value={this.state.detergentType}
                onChange={this.handleChange}
                >
                <option value="Non Drum">Non Drum</option>
                <option value="Drum">Drum</option>
                </select>
            </div>

            <div className="form-group">
                <label className="form-inline">Height</label>
                <input
                type='number'
                className="form-control"
                placeholder='Height in mm'
                name='height'
                value={this.state.height}
                onChange={this.handleChange}
                />
            </div>

            <div className="form-group">
                <label className="form-inline">Internal Heater?</label>
                <select
                className="form-control"
                name='internalHeater'
                value={this.state.internalHeater}
                onChange={this.handleChange}
                >
                <option value="Yes">Yes</option>
                <option value="No">No</option>
                </select>
            </div>

            <div className="form-group">
                <label className="form-inline">Power Consumption in Mode</label>
                <input
                type='number'
                className="form-control"
                placeholder='Enter value in watts'
                name='powerConsMode'
                value={this.state.powerConsMode}
                onChange={this.handleChange}
                />
            </div>

            <div className="form-group">
                <label className="form-inline">Program Name</label>
                <input
                type='text'
                className="form-control"
                placeholder='Name of the Program - normal/cotton etc'
                name='progName'
                value={this.state.progName}
                onChange={this.handleChange}
                />
            </div>

            <div className="form-group">
                <label className="form-inline">Standby Power Usage</label>
                <input
                type='number'
                className="form-control"
                placeholder='Enter value in watts'
                name='standbyPowerUsage'
                value={this.state.standbyPowerUsage}
                onChange={this.handleChange}
                />
            </div>

            <div className="form-group">
                <label className="form-inline">Type</label>
                <select
                className="form-control"
                name='type'
                value={this.state.type}
                onChange={this.handleChange}
                >
                <option value="Drum">Drum</option>
                <option value="Non Drum">Non Drum</option>
                </select>
            </div>

            <div className="form-group">
                <label className="form-inline">Width</label>
                <input
                type='number'
                className="form-control"
                placeholder='Width in mm'
                name='width'
                value={this.state.width}
                onChange={this.handleChange}
                />
            </div>

            <div className="form-group">
                <label className="form-inline">Program Time</label>
                <input
                type='number'
                className="form-control"
                placeholder='Enter time in minutes'
                name='progTime'
                value={this.state.progTime}
                onChange={this.handleChange}
                />
            </div>

            <button
                type='submit'
                className='form-group btn btn-lg btn-success'
                onClick={this.submitForm}
                disabled={this.state.loading}
            >
            {!this.state.loading ? "Find Star Rating" : "Submitting..."}
          </button>
        </form>
        <button className="btn btn-success" onClick={()=>{window.location.href= '/'}}>Back to Home</button>
      </div>
    );

    if(this.state.response){
      content = <Response response={this.state.response} appliance="washing_machine" />
    }
    else content = formContent;
    return <div>{content}</div>;
  }
}

export default WashingMachine;