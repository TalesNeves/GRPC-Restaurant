import grpc
import restaurante_pb2_grpc as pb2_grpc
import restaurante_pb2 as pb2
from concurrent import futures
import time

class RestauranteService(pb2_grpc.SDServicer):
    grill_orders=[]
    kitchen_orders=[]
    bar_orders=[]
    def __init__(self, *args, **kwargs):
        pass
    
    def Garcon2Server(self, request, context):
        items = request.items
        grill_items=[]
        kitchen_items=[]
        bar_items=[]
        for item in items:
            print(item.id)
            if item.id == 1:
                grill_items.append(item)
            elif item.id == 2:
                kitchen_items.append(item)
            elif item.id == 3:
                bar_items.append(item)

        if len(grill_items)>0:
            order_dic={"table":request.table,"items":grill_items}
            order = pb2.Order(**order_dic)
            self.grill_orders.append(order)
        if len(kitchen_items)>0:
            order_dic={"table":request.table,"items":kitchen_items}
            order = pb2.Order(**order_dic)
            print(order)
            self.kitchen_orders.append(order)
        if len(bar_items)>0:
            order_dic={"table":request.table,"items":bar_items}
            order = pb2.Order(**order_dic)
            self.bar_orders.append(order)

        print(self.grill_orders)
        print(self.kitchen_orders)
        print(self.bar_orders)

        response = {'response':'Order taken'}
        return pb2.MensagemResponse(**response)


    def Department2Server(self,request,context):
        client_type = request.department_id
        if client_type == 2:
            return pb2.OrderQeue(orders = self.grill_orders)
        elif client_type == 3:
            return pb2.OrderQeue(orders = self.kitchen_orders)
        elif client_type == 4:
            return pb2.OrderQeue(orders = self.bar_orders)
        return pb2.OrderQeue(orders = [])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_SDServicer_to_server(RestauranteService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    # try:
    #     while True:
    #         print("looop")
    #         time.sleep(10)
    # except KeyboardInterrupt:
    #     print("KeyboardInterrupt")
    #     server.stop(0)
    server.wait_for_termination()

if __name__== '__main__':
    serve()