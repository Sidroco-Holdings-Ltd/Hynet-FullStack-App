from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import powerfactory as pf
app = pf.GetApplication()   

router = APIRouter(prefix="/example", tags=["Example / PowerFactory"])


# --- Request models (aligned with Untitled-1.py) ---

class SymTypeRequest(BaseModel):
    """Change synchronous generator model (standard or classical)."""
    type: str = Field(..., description="Generator model: 'standard' or 'classical'")


class ItemsRequest(BaseModel):
    """Optional list of element names (lines, loads, or generators)."""
    items: Optional[list[str]] = Field(None, description="Element names; omit for all relevant objects")


class LoadingRequest(BaseModel):
    """Loading level for load/generation scaling."""
    loading: float = Field(1.0, ge=0.0, description="Loading factor (e.g. 0.65, 1.0)")


class RandomCasesRequest(BaseModel):
    """Number of random N-2 cases to generate."""
    num: int = Field(..., ge=1, description="Number of random cases")


# --- Endpoints (mirror Untitled-1.py operations) ---

@router.post("/sym-type")
async def change_sym_type(body: SymTypeRequest):
    """Change the model of the synchronous generator (standard/classical)."""
    if body.type not in ("standard", "classical"):
        raise HTTPException(status_code=400, detail="type must be 'standard' or 'classical'")
    return {"action": "ChangeSymType", "type": body.type, "status": "accepted"}


@router.post("/load-type")
async def change_load_type():
    """Change load type parameters (aP, bP, bQ)."""
    return {"action": "ChangeLoadType", "status": "accepted"}


@router.post("/disable-avr")
async def disable_avr():
    """Disable AVR / SEXS / IEEEVC elements."""
    return {"action": "DisableAVR", "status": "accepted"}


@router.post("/overcurrent-relay")
async def add_overcurrent_relay(body: ItemsRequest):
    """Add overcurrent relay to lines/transformers. Optional items list; omit for all."""
    return {"action": "AddOvercurrentRelay", "items": body.items, "status": "accepted"}


@router.delete("/overcurrent-relay")
async def remove_overcurrent_relay(body: ItemsRequest):
    """Remove overcurrent relay from lines/transformers."""
    return {"action": "RemoveOvercurrentRelay", "items": body.items, "status": "accepted"}


@router.post("/under-frequency-load-shedding")
async def add_under_frequency_load_shedding(body: ItemsRequest):
    """Add under-frequency load shedding (UFLS) relay to loads."""
    return {"action": "AddUnderFrequencyLoadShedding", "items": body.items, "status": "accepted"}


@router.delete("/under-frequency-load-shedding")
async def remove_under_frequency_load_shedding(body: ItemsRequest):
    """Remove UFLS relay from loads."""
    return {"action": "RemoveUnderFrequencyLoadShedding", "items": body.items, "status": "accepted"}


@router.post("/over-frequency-generator-tripping")
async def add_over_frequency_generator_tripping(body: ItemsRequest):
    """Add over-frequency generator tripping (OFGT) relay to generators."""
    return {"action": "AddOverFrequencyGeneratorTripping", "items": body.items, "status": "accepted"}


@router.delete("/over-frequency-generator-tripping")
async def remove_over_frequency_generator_tripping(body: ItemsRequest):
    """Remove OFGT relay from generators."""
    return {"action": "RemoveOverFrequencyGeneratorTripping", "items": body.items, "status": "accepted"}


@router.post("/under-frequency-generator-tripping")
async def add_under_frequency_generator_tripping(body: ItemsRequest):
    """Add under-frequency generator tripping (UFGT) relay to generators."""
    return {"action": "AddUnderFrequencyGeneratorTripping", "items": body.items, "status": "accepted"}


@router.delete("/under-frequency-generator-tripping")
async def remove_under_frequency_generator_tripping(body: ItemsRequest):
    """Remove UFGT relay from generators."""
    return {"action": "RemoveUnderFrequencyGeneratorTripping", "items": body.items, "status": "accepted"}


@router.post("/generator-control")
async def set_up_generator_control():
    """Set up generator control (AGC, OutOfStep, Vmea)."""
    return {"action": "SetUpGeneratorControl", "status": "accepted"}


@router.post("/loading-level")
async def change_loading_level(body: LoadingRequest):
    """Change loading level for loads (scaling factor)."""
    return {"action": "ChangeLoadingLevel", "loading": body.loading, "status": "accepted"}


@router.post("/initial-generation-level")
async def change_initial_generation_level(body: LoadingRequest):
    """Change initial generation level (and Pmin_uc scaling)."""
    return {"action": "ChangeInitialGenerationLevel", "loading": body.loading, "status": "accepted"}


@router.post("/line-rating")
async def change_line_rating():
    """Update line ratings from parameters."""
    return {"action": "ChangeLineRating", "status": "accepted"}


@router.post("/random-cases")
async def generate_random_cases(body: RandomCasesRequest):
    """Generate random N-2 contingency cases (weighted choice)."""
    return {"action": "GenerateRandomCases", "num": body.num, "status": "accepted"}


@router.post("/run-n2-contingencies")
async def run_n2_contingencies():
    """Run N-2 contingency simulations (from Random Cases.csv)."""
    import time
    import os
    import pandas as pd

    time_start = time.time()

    Lines = app.GetCalcRelevantObjects("*.ElmLne")
    Ldf = app.GetFromStudyCase('ComLdf')   # Get commands of calculating load flow
    Init = app.GetFromStudyCase('ComInc')  # Get commands of calculating initial conditions
    Sim = app.GetFromStudyCase('ComSim')   # Get commands of running simulations
    ElmRes = app.GetFromStudyCase('Results.ElmRes')  # Create class of result variables named "Results"
    ComRes = app.GetFromStudyCase('ComRes')  # Get commands of export results
    Events_folder = app.GetFromStudyCase('IntEvt')  # Get events folder

    start = 0

    end = 1000
    
    EventSet = Events_folder.GetContents()
    Outage1 = EventSet[0]
    Outage2 = EventSet[1]
    Outage1.outserv = 0
    Outage2.outserv = 0 # switch on the outage event


    data = pd.read_csv("Random Cases.csv", header=None)
    list=data.values.tolist()
    # app.PrintPlain(list[0])
    # app.PrintPlain(list[0][1])
    # app.PrintPlain(len(list))


    for i in range(start, end) :

        app.PrintPlain(i)
        app.PrintPlain(list[i][1:3])


        # Init.Execute()
        #lines1 = np.array(lines)

        for item in Lines:
            if item.loc_name == list[i][1]:
                Outage1.p_target = item # event target is the each line
                Outage1.time = 1.0  # starts at t= 1s
                Outage1.i_what = 0  # take the element out of service
            if item.loc_name == list[i][2]:
                Outage2.p_target = item
                Outage2.time = 1.0  # starts at t= 1s
                Outage2.i_what = 0  # take the element out of service

        Sim.tstop = 300 # simulation time = 300s

        Init.Execute()
        Sim.Execute()
        
        Ldf.Execute()

        time_end = time.time()
        # with open("readme2.csv", 'a', newline='') as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow([i, list[i][1:3], time_end - time_start])
        Window = app.GetOutputWindow()

        Path= r'C:\Users\DayDay\OneDrive - University of Manchester\Yitian\Matpower\0.65\%i-%i.txt'%(start, i)
        # Path= r'C:\Users\44756\OneDrive - UOM\Yitian\Matpower\%i-%i.txt'%(start, i)
        

        Window.Save(Path)
        #app.ClearOutputWindow()
        
        if (i - start) > 0 : 
            Path_old= r'C:\Users\DayDay\OneDrive - University of Manchester\Yitian\Matpower\0.65\%i-%i.txt'%(start, i - 1)
            # Path_old= r'C:\Users\44756\OneDrive - UOM\Yitian\Matpower\%i-%i.txt'%(start, i - 1)
            os.remove(Path_old)
    return {"action": "RunN2Contingencies", "status": "accepted"}


@router.post("/matching")
async def matching():
    """Run matching (static/dynamic data correlation)."""
    return {"action": "matching", "status": "accepted"}


@router.get("/simulation")
async def simulation():
    """Generic simulation entry (e.g. run a predefined sequence)."""
    return {"action": "simulation", "status": "accepted"}
