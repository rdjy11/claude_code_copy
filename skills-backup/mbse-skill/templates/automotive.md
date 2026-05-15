# 汽车领域建模模板

> 本文件为 mbse-modeler 的模板库，Agent 执行建模时直接取用。

## 整车系统上下文模板

```sysml
package VehicleSystemContext {
    private import ScalarValues::*;

    // 外部参与者
    part def Driver;
    part def Road;
    part def Infrastructure;  // V2X
    part def Environment;     // 天气、光照

    // 系统边界
    part def VehicleSystem {
        // 域控制器
        part chassisDomain : ChassisDomainController;
        part adDomain : ADDomainController;
        part cockpitDomain : CockpitDomainController;
        part bodyDomain : BodyDomainController;
        part powerDomain : PowerDomainController;
    }

    // 系统上下文实例
    part vehicleContext {
        part driver : Driver;
        part vehicle : VehicleSystem;
        part road : Road;
        part infra : Infrastructure;
        part env : Environment;

        // 接口连接
        interface driverToVehicle connect driver to vehicle;
        interface vehicleToRoad connect vehicle to road;
        interface vehicleToInfra connect vehicle to infra;
    }
}
```

## ADAS功能建模模板（PPA管线）

```sysml
package AdasFunctionModel {
    private import ScalarValues::*;
    private import ISQ::*;
    private import SI::*;

    // 感知
    action def Perceive {
        in sensorData : SensorFusion;
        out environment : EnvironmentModel;
    }

    // 决策
    action def Plan {
        in environment : EnvironmentModel;
        in route : RoutePlan;
        out trajectory : Trajectory;
    }

    // 执行
    action def Act {
        in trajectory : Trajectory;
        out vehicleControl : ControlCommand;
    }

    // PPA主流程
    action adasPipeline {
        action perceive : Perceive;
        action plan : Plan;
        action act : Act;

        first start then perceive;
        then plan;
        then act;
        then done;

        flow from perceive.environment to plan.environment;
        flow from plan.trajectory to act.trajectory;
    }
}
```
