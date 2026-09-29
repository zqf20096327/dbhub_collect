# tidb-plan-visulation
通过plantuml对tidb的执行计划进行视觉化分析


# 使用方法

##### 代码下载
将src中的代码放入到tidb工程下，pingcap/tidb/plan目录下

##### 增加切入点
plan/session.go 文件中增加sql解析的切入点<br>
````
func (s *session) Execute(ctx context.Context, sql string) (recordSets []ast.RecordSet, err error) {
......
		compiler := executor.Compiler{Ctx: s}
		for _, stmtNode := range stmtNodes {

            // 增加如下代码
			plan.NodeAnalysis(sql,stmtNode)

			s.PrepareTxnCtx(ctx)
......
}
````

plan/optimizer.go 文件中增加逻辑解析和物理解析的切入点
````
func Optimize(ctx sessionctx.Context, node ast.Node, is infoschema.InfoSchema) (Plan, error) {
......
	if logic, ok := p.(LogicalPlan); ok {
	     
	    // 增加逻辑解析
		LogicalPlanAnalysis(node.Text(),logic)
		physicalPlan,error:=doOptimize(builder.optFlag, logic)
		
		// 增加物理解析
		PhysicalPlanAnalysis(node.Text(),physicalPlan)
		return physicalPlan,error
	}
......
}
````

##### 调用输出

在sql语句中增加#uml即会将plantuml格式的结构打印出来
````
select 1 #uml
````

输出结果，每对@startuml和@enduml是一套解析内容。
````
Node Analysis start********************************************************************
@startuml
object ast.SelectStmt_1
object ast.FieldList_2
object ast.SelectField_3
object ast.ValueExpr_4
ast.SelectStmt_1-->ast.FieldList_2
ast.FieldList_2-->ast.SelectField_3
ast.SelectField_3-->ast.ValueExpr_4
@enduml
Node Analysis end********************************************************************
LogicalPlan Analysis start********************************************************************
@startuml
object Projection_2
Projection_2 : type = *plan.LogicalProjection
object TableDual_1
TableDual_1 : type = *plan.LogicalTableDual
Projection_2-->TableDual_1
@enduml
LogicalPlan Analysis end********************************************************************
PhysicalPlan Analysis start********************************************************************
@startuml
object Projection_3
Projection_3 : type = *plan.PhysicalProjection
Projection_3 : task = root
object TableDual_4
TableDual_4 : type = *plan.PhysicalTableDual
TableDual_4 : task = root
Projection_3-->TableDual_4
@enduml
PhysicalPlan Analysis end********************************************************************
````

##### 图形化解析

访问该网站
http://www.plantuml.com/plantuml/form 在线设计器<br>

拷贝@startuml到@enduml内容到录入框中，即可看到分析情况。<br>
也可以选择SVG形式，这样可以放大图像。
