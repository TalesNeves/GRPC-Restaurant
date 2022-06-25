import grpc
import restaurante_pb2_grpc as pb2_grpc
import restaurante_pb2 as pb2
import time



class RestauranteClient(object):


    def __init__(self):
        self.host = 'localhost'
        self.server_port = 50051

        self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.server_port))
        self.stub = pb2_grpc.SDStub(self.channel)

    def send_order(self,Order):
        return self.stub.Garcon2Server(Order)


    def check_qeue(self,client_type):
        request = pb2.DepartmentMessage(department_id=client_type)
        return self.stub.Department2Server(request)

    def get_table_order(self):
        table_id = int(input("Which table are you attending?\n"))
        items = []
        choice = 5
        while choice > 0:
            if(choice<4):
                quantity = int(input("How many?\n"))
                foo= {"id":choice,"quantity":quantity}
                item = pb2.Item(**foo)
                items.append(item)
                # orders.append(item)
                # print(orders)
            choice = int(input("0-Finish Order\n1-Cheeseburguer\n2-L'entrecote du Port \n3-Marguerita\n"))
        order_dic = {"table":table_id,"items":items}
        order = pb2.Order(**order_dic)
        print(order)
        return order

if __name__ == '__main__':
    client = RestauranteClient()
    client_type = 0
    while((client_type<1) or (client_type>4)):
        try:
            client_type= int(input("Open communication as\n1-Garcon Department\n2-Grill Department\n3-Kitchen Department\n4-Bar Department\n"))
        except KeyboardInterrupt:
            break

    
    if client_type==1:
        print("~~Good morning~~")
        try:
                order = client.get_table_order()
                client.send_order(Order=order)
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
    
    else:
        try:
            while True:
                print(client.check_qeue(client_type=client_type))
                time.sleep(5)
        except KeyboardInterrupt:
            print("KeyboardInterrupt")